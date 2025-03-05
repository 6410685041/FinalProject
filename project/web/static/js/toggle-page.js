function toggleSection() {
    var section1 = document.getElementById('section1');
    var section2 = document.getElementById('section2');
    if (section1.style.display === 'block') {
        section1.style.display = 'none';
        section2.style.display = 'block';
    } else {
        section1.style.display = 'block';
        section2.style.display = 'none';
    }
}