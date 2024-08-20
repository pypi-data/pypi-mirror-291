from setuptools import setup, find_packages
from torch.utils.cpp_extension import CppExtension, BuildExtension
import os
import shutil

class CustomBuildExtension(BuildExtension):
    def run(self):
        # Call the parent class's run method
        super().run()
        # Move the shared object to the same directory as setup.py
        for ext in self.extensions:
            build_lib_dir = self.get_ext_fullpath(ext.name)
            target_path = os.path.join(os.path.dirname(__file__), '..', 'plugins.cpython-aarch64-linux-gnu.so')
            shutil.move(build_lib_dir, target_path)
            build_dir = os.path.join(os.path.dirname(__file__), 'build')
            if not os.listdir(build_dir):
                os.rmdir(build_dir)

setup(
    name='trt_pose',
    version='0.0.1',
    description='Pose detection accelerated by NVIDIA TensorRT',
    packages=find_packages(),
    ext_modules=[
        CppExtension(
            'plugins',
            [
                'trt_pose/parse/find_peaks.cpp',
                'trt_pose/parse/paf_score_graph.cpp',
                'trt_pose/parse/refine_peaks.cpp',
                'trt_pose/parse/munkres.cpp',
                'trt_pose/parse/connect_parts.cpp',
                'trt_pose/plugins.cpp',
                'trt_pose/train/generate_cmap.cpp',
                'trt_pose/train/generate_paf.cpp',
            ]
        )
    ],
    cmdclass={'build_ext': CustomBuildExtension},
)

