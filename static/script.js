document.getElementById('help-button').addEventListener('click', function() {
    var helpText = document.getElementById('help-text');
    if (helpText.style.display === 'none') {
        helpText.style.display = 'block';
    } else {
        helpText.style.display = 'none';
    }
});
