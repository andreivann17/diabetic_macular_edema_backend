from pydicom import dcmread
from pydicom.dataset import Dataset
from pydicom.uid import ExplicitVRLittleEndian,generate_uid
from pydicom.dataset import Dataset, FileMetaDataset
from PIL import Image
import numpy as np
import base64

def get(name):
    ds = dcmread(f'{name}.dcm')
    print(ds)

def create(patient_id):
    image_path = f'media/detections/{id_patient}.jpg'
    # Create some metadata elements
    file_meta = FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'  # Change this to the correct value for your type of DICOM file
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.ImplementationClassUID = '1.2.3.4.5.6.7.8.9.0'
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian  # This was missing before

    # Create the Dataset
    ds = Dataset()
    ds.file_meta = file_meta

    # Add the Data Elements -- not all of these are required, these are just examples
    ds.PatientName = patient_name
    ds.PatientID = patient_id

    # Modality
    ds.Modality = 'OP'
    ds.SeriesInstanceUID = generate_uid()
    ds.SOPInstanceUID = generate_uid()

    # Set the transfer syntax
    ds.is_little_endian = True
    ds.is_implicit_VR = False

    # Load the image and convert it to a NumPy array
    img = Image.open(image_path)
    img_array = np.array(img)

    # Set Pixel Data
    ds.PixelData = img_array.tobytes()

    # Save the dataset
    ds.save_as("andre.dcm", write_like_original=False)

    return ds
def dicom_to_jpg():
    ds = dcmread('andre.dcm')
    new_image = ds.pixel_array.astype(float)
    scaled_image = (np.maximum(new_image, 0) / new_image.max()) * 255.0
    scaled_image = np.uint8(scaled_image)
    final_image = Image.fromarray(scaled_image)
    return final_image

def dicom_to_base64(file_path):
    with open(file_path, 'rb') as dicom_file:
        return base64.b64encode(dicom_file.read()).decode('utf-8')


