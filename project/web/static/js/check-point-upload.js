document.getElementById("upload-task").onsubmit = function(event) {
    console.log("Submitting form...");
    const image = document.getElementById("image").value;
    const video = document.getElementById("video").value;
    const collectedTime = document.getElementById("collected_time").value;
    if (!image && !video) {
        alert("Please input image or video");
        event.preventDefault(); // Prevent form submission
    } else if (collectedTime) {
        const currentDate = new Date();
        const inputDate = new Date(collectedTime);
        
        // Check if the input date is in the future
        if (inputDate > currentDate) {
            alert("The collected date should be today or in the past.");
            event.preventDefault(); // Prevent form submission
        } else {
            event.target.submit();
        }
    }
};