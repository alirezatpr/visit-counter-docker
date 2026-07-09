const API_URL = 'http://localhost:5000/api/visit';

async function fetchVisit() {
    try {
        const response = await fetch(API_URL);
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('message').textContent = data.message;
            document.getElementById('counter').textContent = data.visit_count;
            document.getElementById('ip').textContent = 'IP: ' + data.ip;
        } else {
            document.getElementById('message').textContent = 'خطا در دریافت اطلاعات';
            document.getElementById('counter').textContent = '❌';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('message').textContent = 'خطا در اتصال به سرور';
        document.getElementById('counter').textContent = '⚠️';
    }
}

function refreshVisit() {
    document.getElementById('message').textContent = 'در حال بارگذاری...';
    document.getElementById('counter').textContent = '⏳';
    fetchVisit();
}

// بارگذاری اولیه
window.onload = fetchVisit;
