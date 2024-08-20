import cv2, ctypes
import PIL.Image
import os, sys
import subprocess
import logging
import json
import time
import numpy as np
import ipywidgets.widgets as widgets
from IPython.display import display
import __main__


logging.basicConfig(
    format='%(asctime)s - [%(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%m/%d/%Y %I:%M:%S %p',
)
isnotebook = __main__.isnotebook

def bgr8_to_jpeg(value):
    return bytes(cv2.imencode(".jpg", value)[1])

def import_tensorflow():
    global tf, K
    import tensorflow as tf
    import tensorflow.keras as __module
    import keras.backend as K
    
    for k in [m for m in dir(__module) if not "__" in m]:
        globals()[k]=__module.__dict__[k]

    import tensorflow.keras.models as __module
    
    for k in [m for m in dir(__module) if not "__" in m]:
        globals()[k]=__module.__dict__[k]

    import tensorflow.keras.losses as __module
    
    for k in [m for m in dir(__module) if not "__" in m]:
        globals()[k]=__module.__dict__[k]

    import tensorflow.keras.layers as __module
    
    for k in [m for m in dir(__module) if not "__" in m]:
        globals()[k]=__module.__dict__[k]

    import tensorflow.keras.optimizers as __module
    
    for k in [m for m in dir(__module) if not "__" in m]:
        globals()[k]=__module.__dict__[k]
        
    import tensorflow.keras.callbacks as __module
    
    for k in [m for m in dir(__module) if not "__" in m]:
        globals()[k]=__module.__dict__[k]

    import tensorflow.keras.utils as __module
    
    for k in [m for m in dir(__module) if not "__" in m]:
        globals()[k]=__module.__dict__[k]

    gpus=tf.config.experimental.list_physical_devices('GPU')

    if gpus:
        try:
            tf.config.set_visible_devices(gpus[0], 'GPU')
        except RuntimeError as e:
            logging.error(e)
            
def scheduler(epoch, learningrate):
    if epoch < 100:
        return learningrate
    else:
        return learningrate * tf.math.exp(-0.1)

class Object_Follow():
    list_path = os.path.abspath(__file__ + "/../lists/object.names")
    with open(list_path) as f:
        lines = f.readlines()
        label_list = [line.rstrip('\n') for line in lines]

    def __init__(self, camera=None, label_list=None):
        global trt, cuda
        import tensorrt as trt
        import pycuda.driver as cuda
        import pycuda.autoinit
        
        self.camera = camera
        self.default_path = os.path.abspath(__file__ + "/../models/yolov4-tiny/")

        if label_list != None:
            self.label_list = label_list

        if isnotebook:
            if camera is not None:
                self.probWidget = widgets.Image(
                    format="jpeg", width=camera.width, height=camera.height
                )
            else:
                self.probWidget = widgets.Image(
                    format="jpeg", width=300, height=300
                )
        else:
            self.probWidget = None
        
        self.cls_dict = {i: n for i, n in enumerate(self.label_list)}

    def __allocate_buffers(self, engine):
        inputs = []
        outputs = []
        bindings = []
        output_idx = 0
        stream = cuda.Stream()

        class HostDeviceMem(object):
            def __init__(self, host_mem, device_mem):
                self.host = host_mem
                self.device = device_mem

            def __repr__(self):
                return "Host:\n" + str(self.host) + "\nDevice:\n" + str(self.device)

        for binding in engine:
            binding_dims = engine.get_binding_shape(binding)
            if len(binding_dims) == 4:
                size = trt.volume(binding_dims)
            elif len(binding_dims) == 3:
                size = trt.volume(binding_dims) * engine.max_batch_size
            else:
                raise ValueError(
                    "bad dims of binding %s: %s" % (binding, str(binding_dims))
                )
            dtype = trt.nptype(engine.get_binding_dtype(binding))
            host_mem = cuda.pagelocked_empty(size, dtype)
            device_mem = cuda.mem_alloc(host_mem.nbytes)
            bindings.append(int(device_mem))
            if engine.binding_is_input(binding):
                inputs.append(HostDeviceMem(host_mem, device_mem))
            else:
                assert size % 7 == 0
                outputs.append(HostDeviceMem(host_mem, device_mem))
                output_idx += 1
        assert len(inputs) == 1
        assert len(outputs) == 1
        return inputs, outputs, bindings, stream

    def __preprocess_yolo(self, img, input_shape):
        img = cv2.resize(img, (input_shape[1], input_shape[0]))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.transpose((2, 0, 1)).astype(np.float32)
        img /= 255.0
        return img

    def __postprocess_yolo(
        self, trt_outputs, img_w, img_h, conf_th, nms_threshold, input_shape
    ):
        detections = []
        for o in trt_outputs:
            dets = o.reshape((-1, 7))
            dets = dets[dets[:, 4] * dets[:, 6] >= conf_th]
            detections.append(dets)
        detections = np.concatenate(detections, axis=0)

        if len(detections) == 0:
            boxes = np.zeros((0, 4), dtype=np.int)
            scores = np.zeros((0,), dtype=np.float32)
            classes = np.zeros((0,), dtype=np.float32)
        else:
            old_h, old_w = img_h, img_w
            detections[:, 0:4] *= np.array(
                [old_w, old_h, old_w, old_h], dtype=np.float32
            )

            nms_detections = np.zeros((0, 7), dtype=detections.dtype)
            for class_id in set(detections[:, 5]):
                idxs = np.where(detections[:, 5] == class_id)
                cls_detections = detections[idxs]

                x_coord = cls_detections[:, 0]
                y_coord = cls_detections[:, 1]
                width = cls_detections[:, 2]
                height = cls_detections[:, 3]
                box_confidences = cls_detections[:, 4] * cls_detections[:, 6]

                areas = width * height
                ordered = box_confidences.argsort()[::-1]

                keep = list()
                while ordered.size > 0:
                    i = ordered[0]
                    keep.append(i)
                    xx1 = np.maximum(x_coord[i], x_coord[ordered[1:]])
                    yy1 = np.maximum(y_coord[i], y_coord[ordered[1:]])
                    xx2 = np.minimum(
                        x_coord[i] + width[i], x_coord[ordered[1:]] + width[ordered[1:]]
                    )
                    yy2 = np.minimum(
                        y_coord[i] + height[i],
                        y_coord[ordered[1:]] + height[ordered[1:]],
                    )

                    width1 = np.maximum(0.0, xx2 - xx1 + 1)
                    height1 = np.maximum(0.0, yy2 - yy1 + 1)
                    intersection = width1 * height1
                    union = areas[i] + areas[ordered[1:]] - intersection
                    iou = intersection / union
                    indexes = np.where(iou <= nms_threshold)[0]
                    ordered = ordered[indexes + 1]

                keep = np.array(keep)
                nms_detections = np.concatenate(
                    [nms_detections, cls_detections[keep]], axis=0
                )

            xx = nms_detections[:, 0].reshape(-1, 1)
            yy = nms_detections[:, 1].reshape(-1, 1)
            ww = nms_detections[:, 2].reshape(-1, 1)
            hh = nms_detections[:, 3].reshape(-1, 1)
            boxes = np.concatenate([xx, yy, xx + ww, yy + hh], axis=1) + 0.5
            boxes = boxes.astype(np.int)
            scores = nms_detections[:, 4] * nms_detections[:, 6]
            classes = nms_detections[:, 5]
        return boxes, scores, classes

    def __inference_fn(self, context, bindings, inputs, outputs, stream):
        [cuda.memcpy_htod_async(inp.device, inp.host, stream) for inp in inputs]
        context.execute_async_v2(bindings=bindings, stream_handle=stream.handle)
        [cuda.memcpy_dtoh_async(out.host, out.device, stream) for out in outputs]
        stream.synchronize()
        return [out.host for out in outputs]

    def __draw_bboxes(self, img, boxes, clss, confs, idx, mx):
        for i, (bb, cl, cf) in enumerate(zip(boxes, clss, confs)):
            cl = int(cl)
            # if (cl != 12) and (cl != 13):
            x_min, y_min, x_max, y_max = bb[0], bb[1], bb[2], bb[3]
            if cl == idx and i == mx:
                box_color = (0, 255, 0)
                text_color = (0, 0, 0)
            else:
                box_color = (255, 0, 0)
                text_color = (255, 255, 255)
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), box_color, 2)
            txt_loc = (max(x_min + 2, 0), max(y_min + 2, 0))
            cls_name = self.cls_dict.get(cl, "CLS{}".format(cl))
            txt = "{} {:.2f}".format(cls_name, cf)
            img_h, img_w, _ = img.shape
            if txt_loc[0] >= img_w or txt_loc[1] >= img_h:
                return img
            margin = 3
            size = cv2.getTextSize(txt, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            w = size[0][0] + margin * 2
            h = size[0][1] + margin * 2
            cv2.rectangle(
                img, (x_min - 1, y_min - 1 - h), (x_min + w, y_min), box_color, -1
            )
            cv2.putText(
                img,
                txt,
                (x_min + margin, y_min - margin - 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                text_color,
                lineType=cv2.LINE_AA,
            )
        return img
    
    def generate_trt(self, model_path=None):
        self.layer_path = os.path.join(self.default_path, "libyolo_layer.so")
        if not os.path.exists(self.layer_path):
            ori_dir = os.getcwd()
            os.chdir(os.path.join(self.default_path, "plugins"))
            subprocess.run(['make'])
            os.chdir(ori_dir)
            
        from .yolo2trt import yolo_to_onnx
        from .yolo2trt import onnx_to_trt
        
        if model_path is None:
            import gdown
            model_path = os.path.join(self.default_path, "yolov4-tiny")
                        
            ori_dir = os.getcwd()
            os.chdir(self.default_path)
            if not os.path.exists(os.path.join(self.default_path, "yolov4-tiny.cfg")):
                gdown.download('https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg', 'yolov4-tiny.cfg', quiet=False)
            if not os.path.exists(os.path.join(self.default_path, "yolov4-tiny.weights")):
                gdown.download('https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.weights', 'yolov4-tiny.weights', quiet=False)
            os.chdir(ori_dir)
            
        ori_dir = os.getcwd()
        path = os.path.dirname(model_path)
        model = os.path.basename(model_path)
        model_name, model_format = os.path.splitext(model)
        
        if model_format:
            logging.warning("Please do not include the model's extension.")
            return 
        elif os.path.exists(os.path.join(path, model_name) + ".trt"):
            logging.warning(f"{model_name}.trt already exists.")
            return
        
        os.chdir(path)
        yolo_to_onnx.convert(model_name)
        onnx_to_trt.convert(model_name)
        os.chdir(ori_dir)

    def load_model(self, path=None):
        self.layer_path = os.path.join(self.default_path, "libyolo_layer.so")
        if not os.path.exists(self.layer_path):
            ori_dir = os.getcwd()
            os.chdir(os.path.join(self.default_path, "plugins"))
            subprocess.run(['make'])
            os.chdir(ori_dir)
        try:
            ctypes.cdll.LoadLibrary(self.layer_path)
        except OSError as e:
            raise SystemExit("ERROR: failed to load layer file.") from e
        
        if path is None:
            self.model_path = os.path.join(self.default_path, "yolov4-tiny.trt")
            if not os.path.exists(self.model_path):
                logging.info("YOLO trt model does not exist. Please, run generate_trt() first.")
        else:
            self.model_path = path

        self.trt_logger = trt.Logger(trt.Logger.INFO)
        with open(self.model_path, "rb") as f, trt.Runtime(self.trt_logger) as runtime:
            self.engine = runtime.deserialize_cuda_engine(f.read())
        if not self.engine:
            raise ValueError("failed to deserialize the engine.")

        binding = self.engine[0]
        binding_dims = self.engine.get_binding_shape(binding)
        try:
            self.input_shape = tuple(binding_dims[2:])
        except:
            raise ValueError(
                "bad dims of binding %s: %s" % (binding, str(binding_dims))
            )

        try:
            self.context = self.engine.create_execution_context()
            self.inputs, self.outputs, self.bindings, self.stream = (
                self.__allocate_buffers(self.engine)
            )
        except Exception as e:
            raise RuntimeError("fail to allocate CUDA resources") from e

    def show(self):
        display(self.probWidget)

    def detect(self, image=None, index=None, threshold=0.5, show=True, callback=None):
        if image is None:
            if self.camera is not None:
                image = self.camera.value
            else:
                raise logging.error("No Camera is available")

        width = image.shape[1]
        height = image.shape[0]

        if type(index) == str:
            try:
                index = self.label_list.index(index)
            except ValueError:
                logging.error("Index is not available.")
                return

        img_resized = self.__preprocess_yolo(image, self.input_shape)
        self.inputs[0].host = np.ascontiguousarray(img_resized)

        self.trt_outputs = self.__inference_fn(
            self.context, self.bindings, self.inputs, self.outputs, self.stream
        )
        boxes, scores, classes = self.__postprocess_yolo(
            self.trt_outputs,
            width,
            height,
            threshold,
            nms_threshold=0.5,
            input_shape=self.input_shape,
        )
        boxes[:, [0, 2]] = np.clip(boxes[:, [0, 2]], 0, width - 1)
        boxes[:, [1, 3]] = np.clip(boxes[:, [1, 3]], 0, height - 1)

        detections = []
        raw_value = []
        for bb, cl in zip(boxes, classes):
            detections.append(
                {
                    "label": int(cl),
                    "bbox": [
                        round(bb[0] / (width / 2) - 1, 2),
                        round(bb[1] / (height / 2) - 1, 2),
                        round(bb[2] / (width / 2) - 1, 2),
                        round(bb[3] / (height / 2) - 1, 2),
                    ],
                    "x": round(((bb[0] + bb[2]) / 2) / (width / 2) - 1, 5),
                    "y": round(((bb[1] + bb[3]) / 2) / (height / 2) - 1, 5),
                    "size_rate": round(
                        (bb[2] - bb[0]) * (bb[3] - bb[1]) / (width * height), 5
                    ),
                }
            )
            raw_value.append([int(cl), bb.tolist()])

        max_size = None
        if index is None:
            result = []
            for det in detections:
                result.append({"label": det["label"], "bbox": det["bbox"]})
        else:
            matching_detections = [d for d in detections if d["label"] == index]

            sizes = [
                det["size_rate"] for det in matching_detections if det["label"] == index
            ]
            if len(sizes) > 0:
                max_size = np.array(sizes).argmax()
                result = matching_detections[max_size]
                result.pop("label")
                result.pop("bbox")
            else:
                result = None

        if show:
            image = self.__draw_bboxes(image, boxes, classes, scores, index, max_size)
            if isnotebook:
                self.probWidget.value = bgr8_to_jpeg(image)
            self.value = image
        self.raw_value = raw_value

        return result

class Track_Follow():
    def __init__(self,camera=None):
        import_tensorflow()
        self.camera = camera
        self.default_path = os.path.abspath(__file__ + "/../models/Track_Follow/Track_Follow.h5")
        self.model = None
        if isnotebook:
            if camera is not None:
                self.probWidget = widgets.Image(
                    format="jpeg", width=camera.width, height=camera.height
                )
            else:
                self.probWidget = widgets.Image(
                    format="jpeg", width=300, height=300
                )
        else:
            self.probWidget = None

    def __load_layers(self):        
        def mish(x):
            return x * K.tanh(K.softplus(x))

        input1 = Input(shape=(150, 300, 3,))
        conv1 = Conv2D(filters=16, kernel_size=(3, 3), strides=(2, 2), padding="same")(input1)
        norm1 = BatchNormalization()(conv1)
        act1 = Activation(mish)(norm1)
        pool1 = MaxPooling2D(pool_size=(3, 3), strides=(2, 2))(act1)
        conv2 = Conv2D(filters=32, kernel_size=(3, 3), strides=(2, 2), padding="same")(pool1)
        norm2 = BatchNormalization()(conv2)
        act2 = Activation(mish)(norm2)
        conv3 = Conv2D(filters=32, kernel_size=(3, 3), strides=(1, 1), padding="same")(act2)
        norm3 = BatchNormalization()(conv3)
        act3 = Activation(mish)(norm3)
        add1 = Add()([act2, act3])
        conv4 = Conv2D(filters=64, kernel_size=(3, 3), strides=(2, 2), padding="same")(add1)
        norm4 = BatchNormalization()(conv4)
        act4 = Activation(mish)(norm4)
        conv5 = Conv2D(filters=64, kernel_size=(3, 3), strides=(1, 1), padding="same")(act4)
        norm5 = BatchNormalization()(conv5)
        act5 = Activation(mish)(norm5)
        add2 = Add()([act4, act5])
        conv6 = Conv2D(filters=128, kernel_size=(3, 3), strides=(2, 2), padding="same")(add2)
        norm6 = BatchNormalization()(conv6)
        act6 = Activation(mish)(norm6)
        conv7 = Conv2D(filters=128, kernel_size=(3, 3), strides=(1, 1), padding="same")(act6)
        norm7 = BatchNormalization()(conv7)
        act7 = Activation(mish)(norm7)
        add3 = Add()([act6, act7])
        conv8 = Conv2D(filters=256, kernel_size=(3, 3), strides=(2, 2), padding="same")(add3)
        norm8 = BatchNormalization()(conv8)
        act8 = Activation(mish)(norm8)
        conv9 = Conv2D(filters=512, kernel_size=(3, 3), strides=(2, 2), padding="same")(act8)
        norm9 = BatchNormalization()(conv9)
        act9 = Activation(mish)(norm9)
        flat1 = Flatten()(act9)
        dense1 = Dense(128)(flat1)
        norm10 = BatchNormalization()(dense1)
        act10 = Activation(mish)(norm10)
        dense2 = Dense(64)(act10)
        norm11 = BatchNormalization()(dense2)
        act11 = Activation(mish)(norm11)
        dense3 = Dense(64)(act11)
        norm12 = BatchNormalization()(dense3)
        act12 = Activation(mish)(norm12)
        dense4 = Dense(2, activation="tanh")(act12)

        self.model = Model(inputs=input1, outputs=dense4)
        
    def load_model(self,path=None):
        if path is None:
            path = self.default_path
            if not os.path.exists(path):
                import gdown
                
                ori_dir = os.getcwd()
                os.chdir(os.path.dirname(path))
                gdown.download('https://drive.google.com/uc?id=1rWF2iF556ntPM3EzDSpwzaDP_CEnLIG0', "Track_Follow.h5", quiet=False)
                os.chdir(ori_dir)
        elif not os.path.exists(path):
            logging.warning(f"{path} doesn't exist.")
            return

        if self.model is None:            
            self.__load_layers()
            opt = Adam()
            self.model.compile(optimizer=opt, loss='MAE')            
            self.model.optimizer.lr.numpy()

        self.model.load_weights(path)

    def show(self):
        display(self.probWidget)

    def run(self, value=None, callback=None):
        if self.model is None :
            logging.warning("Please load a trained model with load_model() method.")
            return
        
        img = self.camera.value if value is None else value
        crop_img = img[130:280,:300]
        x, y = self.model.predict(np.array([crop_img]).astype(np.float32))[0]
        height, width, _ = crop_img.shape
        
        if isnotebook:
            cX = int(width * (x / 2.0 + 0.5))
            cX = max(0, min(cX, 300))
            cY = 150
            self.value = cv2.circle(img, (cX, cY), 6, (255, 0, 0), 2)
            self.probWidget.value = bgr8_to_jpeg(self.value)

        if callback is not None:
            callback(result)
            
        result={"x":x,"y":y}

        return result
    
class PoseNet():
    def __init__(self,camera=None):
        global torch, transforms
        import torch
        import torchvision.transforms as transforms
        from .torch2trt.parse_objects import ParseObjects
        
        self.camera = camera
        self.default_path = os.path.abspath(__file__ + "/../models/trtpose")
        if isnotebook:
            if camera is not None:
                self.probWidget = widgets.Image(
                    format="jpeg", width=camera.width, height=camera.height
                )
            else:
                self.probWidget = widgets.Image(
                    format="jpeg", width=300, height=300
                )
        else:
            self.probWidget = None
        
        self.WIDTH = 224
        self.HEIGHT = 224
        self.X_compress = 300.0 / self.WIDTH * 1.0
        self.Y_compress = 300.0 / self.HEIGHT * 1.0
        self.color = (0, 255, 0)
        
        self.mean = torch.Tensor([0.485, 0.456, 0.406]).cuda()
        self.std = torch.Tensor([0.229, 0.224, 0.225]).cuda()
        self.device = torch.device('cuda')
        self.human_pose = None
        self.topology = self.__topology()
        self.parse_objects = ParseObjects(self.topology)
        
    def __topology(self):
        json_path = os.path.join(self.default_path, "human_pose.json")
        
        with open(json_path, 'r') as f:
            self.human_pose = json.load(f)
            
        return self.__coco2topology(self.human_pose)
        
    def __coco2topology(self, coco_category):
        skeleton = coco_category['skeleton']
        K = len(skeleton)
        topology = torch.zeros((K, 4)).int()
        for k in range(K):
            topology[k][0] = 2 * k
            topology[k][1] = 2 * k + 1
            topology[k][2] = skeleton[k][0] - 1
            topology[k][3] = skeleton[k][1] - 1
        return topology
    
    def __preprocess(self, image):
        image = cv2.resize(image, dsize=(self.WIDTH, self.HEIGHT), interpolation=cv2.INTER_AREA)
                
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = PIL.Image.fromarray(image)
        image = transforms.functional.to_tensor(image).to(self.device)
        image.sub_(self.mean[:, None, None]).div_(self.std[:, None, None])
        return image[None, ...]
    
    def __get_keypoint(self, humans, hnum, peaks):
        kpoint = []
        human = humans[0][hnum]
        C = human.shape[0]
        for j in range(C):
            k = int(human[j])
            if k >= 0:
                peak = peaks[0][j][k]   # peak[1]:width, peak[0]:height
                peak = (j, float(peak[0]), float(peak[1]))
                kpoint.append(peak)
            else:    
                peak = (j, None, None)
                kpoint.append(peak)
        return kpoint
    
    def torch2trt(self, path=None):
        if path is None:
            path = os.path.join(self.default_path, "resnet18_baseline_att_224x224_A_epoch_249.pth")
            
            if not os.path.exists(path):
                import gdown
                
                ori_dir = os.getcwd()
                os.chdir(self.default_path)
                gdown.download('https://drive.google.com/uc?id=1XYDdCUdiF2xxx4rznmLb62SdOUZuoNbd', "resnet18_baseline_att_224x224_A_epoch_249.pth", quiet=False)
                os.chdir(ori_dir)
        elif not os.path.exists(path):
            logging.warning(f"{path} doesn't exist.")
            return
            
        from . import torch2trt 
        from .torch2trt import models
        
        num_parts = len(self.human_pose['keypoints'])
        num_links = len(self.human_pose['skeleton'])

        data = torch.zeros((1, 3, self.HEIGHT, self.WIDTH)).cuda()
        trt_path = path.replace('.pth', '_trt.pth')
        
        if os.path.exists(trt_path):
            logging.warning(f"{os.path.basename(trt_path)} already exists.")
            return
        
        model = models.resnet18_baseline_att(num_parts, 2 * num_links).cuda().eval()
        result = model.load_state_dict(torch.load(path))
        logging.info(f"{result}")
        logging.info("Converting the model now. This may take a while")
        self.model = torch2trt.torch2trt(model, [data], fp16_mode=True, max_workspace_size=1<<25)
        
        
        torch.save(self.model.state_dict(), trt_path)
        logging.info("Model is successfully converted")
        
    def load_model(self, path=None):
        if path is None:
            path = os.path.join(self.default_path, "resnet18_baseline_att_224x224_A_epoch_249_trt.pth")
            
            if not os.path.exists(path):
                logging.warning("There is no trt model. Please, run torch2trt() first.")
                return
        elif not os.path.exists(path):
            logging.warning(f"{path} doesn't exist.")
            return

        from .torch2trt import trt_module

        self.model = trt_module.TRTModule()
        self.model.load_state_dict(torch.load(path))

    def show(self):
        display(self.probWidget)

    def run(self, value=None, callback=None):
        if self.model is None :
            logging.warning("Please load a trained model using load_model() method.")
            return
        
        img = self.camera.value if value is None else value
        frame = img.copy()
        data = self.__preprocess(frame)
        cmap, paf = self.model(data)
        cmap, paf = cmap.detach().cpu(), paf.detach().cpu()
        counts, objects, peaks = self.parse_objects(cmap, paf)
        
        for i in range(counts[0]):
            keypoints = self.__get_keypoint(objects, i, peaks)
            for j in range(len(keypoints)):
                if keypoints[j][1]:
                    x = round(keypoints[j][2] * self.WIDTH * self.X_compress)
                    y = round(keypoints[j][1] * self.HEIGHT * self.Y_compress)
                    cv2.circle(frame, (x, y), 3, self.color, 2)
                    cv2.putText(frame , "%d" % int(keypoints[j][0]), (x + 5, y),  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1)
                    cv2.circle(frame, (x, y), 3, self.color, 2)
                    
        if isnotebook:
            self.probWidget.value = bgr8_to_jpeg(frame)

        return frame