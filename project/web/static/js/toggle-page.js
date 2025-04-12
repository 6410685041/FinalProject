function toggleSection() {
    // Check if all required inputs in section1 are filled
    const section1Inputs = document.querySelectorAll('#section1 .section-background input[required]');
    const isValidSection1 = Array.from(section1Inputs).every(input => input.value.trim() !== '');

    if (isValidSection1) {
        // All inputs are valid, toggle to the next section
        document.getElementById('section1').style.display = 'none';
        document.getElementById('section2').style.display = 'block';
    }
}