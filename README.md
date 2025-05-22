## ErinEyesTextureConverter
* Detects and extracts eyeballs from **images** or **textures**, and converts them into eye textures compatible with the Erin Race in Skyrim.
* Uses a `YOLO11m` model trained on around 300 images.

## How to use
* Clone this repository or download it as a ZIP file.
* Unzip the file and create an `input` directory.
* Place the image files you want to convert (`.dds`, `.png`, `.jpg`, `.jpeg`) into the `input` directory.
* Run either `Run.bat`(for CPU) or `Run_cuda.bat`(for GPU) file.
* Converted textures are saved in the `output` directory.

## Requirements
* Python >= 3.8
* Dependencies are automatically installed when you run `Run.bat` or `Run_cuda.bat`.

## Dependencies
* ultralytics
* pytorch
* opencv-python
* numpy
* pillow
* imageio

## ⚠️Switch between CPU and GPU (CUDA) acceleration
1. Open CMD.
2. Enter `pip uninstall torch torchvision torchaudio`.
3. Enter `y` or `yes` to confirm all uninstall promprts.
4. Run either `Run.bat`(for CPU) or `Run_cuda.bat`(for GPU) file.

---

## 에린 눈 텍스쳐 변환기
* **이미지** 또는 **텍스쳐**에서 눈동자를 감지하고 추출하여 스카이림의 에린 레이스와 호환되는 텍스쳐로 변환합니다.
* `YOLO11m` 모델을 사용하여 약 300여장의 이미지로 학습되었습니다.

## 사용 방법
* 리포지토리를 복제하거나 zip으로 다운로드 합니다
* 압축을 풀고 `input` 디렉토리를 만듭니다.
* 변환하고 싶은 이미지 파일(`.dds`, `.png`, `.jpg`, `.jpeg`)들을 `input` 디렉토리에 넣습니다.
* `Run.bat`(CPU 용) 또는 `Run_cuda.bat`(GPU 용) 파일을 실행합니다.
* 변환 된 텍스쳐는 `output` 디렉토리에 저장됩니다.

## 필수 사항
* 파이썬 3.8 이상
* 종속성은 `Run.bat`또는 `Run_cuda.bat`을 실행 할 때 자동으로 설치 됩니다.

## 종속성
* ultralytics
* pytorch
* opencv-python
* numpy
* pillow
* imageio

## ⚠️CPU 혹은 GPU (CUDA) 가속으로 전환하려면
* CMD를 엽니다
* `pip uninstall torch torchvision torchaudio` 입력합니다.
* 삭제에 대해 묻는 것에 전부 `y` 또는 `yes` 를 입력합니다.
* `Run.bat`(CPU 용) 또는 `Run_cuda.bat`(GPU 용) 파일을 실행합니다.