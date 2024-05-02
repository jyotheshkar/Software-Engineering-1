document.getElementById('downloadBtn').addEventListener('click', function() {
    // Replace 'your_local_exe_path' with the actual local path of your .exe file
    var localExePath = 'zoom.exe'; // Example local .exe file path
    var fileName = 'your-software-setup.exe'; // Name of the .exe file to be downloaded

    // Create a hidden anchor element
    var downloadLink = document.createElement('a');
    downloadLink.href = localExePath;
    downloadLink.download = fileName;
    downloadLink.style.display = 'none'; // Hide the anchor element

    // Append the anchor element to the body and trigger the download
    document.body.appendChild(downloadLink);
    downloadLink.click();

    // Remove the anchor element from the body after download
    document.body.removeChild(downloadLink);
});
