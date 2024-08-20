document.addEventListener('DOMContentLoaded', function () {
    const socket = io();

    const searchBox = document.getElementById('search-box');
    const lineLimit = document.getElementById('line-limit');
    const fileContent = document.getElementById('file-content');
    const darkModeToggle = document.getElementById('dark-mode-toggle');

    // Load preferences or set defaults
    const theme = localStorage.getItem('theme') || 'light';
    const linesPreference = localStorage.getItem('lineLimit') || '30';

    // Apply theme
    if (theme === 'dark') {
        document.body.classList.add('dark-mode');
        darkModeToggle.checked = true;
    } else {
        document.body.classList.remove('dark-mode');
        darkModeToggle.checked = false;
    }

    // Set line limit field value
    lineLimit.value = linesPreference;

    let fullLog = ''; // Store the entire log
    let searchActive = false;
    let searchResults = [];

    function applySearch(query) {
        const lines = fullLog.split('\n');
        searchResults = lines.filter(line => line.toLowerCase().includes(query));
        updateFileContent();
        searchActive = true;
    }

    function updateFileContent() {
        const limit = parseInt(lineLimit.value, 10) || 30; // Default to 30 if empty or invalid
        const linesToShow = searchActive ? searchResults : fullLog.split('\n');
        fileContent.textContent = linesToShow.slice(-limit).join('\n');
        fileContent.scrollTop = fileContent.scrollHeight; // Autoscroll to the bottom
    }

    function updateContent(log) {
        fullLog += log;
        if (searchActive) {
            applySearch(searchBox.value.toLowerCase());
        } else {
            updateFileContent();
        }
    }

    socket.on('connect', function () {
        socket.emit('start_stream');
    });

    socket.on('file_update', function (data) {
        updateContent(data);
    });

    searchBox.addEventListener('input', function () {
        const query = searchBox.value.toLowerCase();
        applySearch(query);
    });

    lineLimit.addEventListener('blur', function () {
        // Only enforce the default value after the user finishes typing
        if (lineLimit.value === '' || parseInt(lineLimit.value, 10) === 0) {
            lineLimit.value = '30';
        }
        updateFileContent();
        localStorage.setItem('lineLimit', lineLimit.value);  // Save preference
    });

    darkModeToggle.addEventListener('click', function () {
        document.body.classList.toggle('dark-mode');
        const newTheme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
        localStorage.setItem('theme', newTheme);  // Save preference
    });
});

