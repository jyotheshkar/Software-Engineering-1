from face_auth import FaceAuthentication

# Create an instance of the FaceAuthentication class
face_auth = FaceAuthentication()

# Authentication key is created upon storing the users face for the first time. Files will be overwritten everytime store_face is called, so it can be called once more to reset if the users requires it.

# Call the store_face method to store the users face for future authentication (encrypted within a .bin file)
result_store = face_auth.store_face()
print(result_store)

# Call the compare_face method to authenticate the users face with their previously encypted face from the .bin file
result_compare = face_auth.compare_face()
print(result_compare)
