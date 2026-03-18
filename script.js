document.getElementById('playBtn').addEventListener('click', async function() {
    const inputUrl = document.getElementById('teralink').value.trim();
    const loading = document.getElementById('loading');
    const playerCard = document.getElementById('player-card');
    const video = document.getElementById('mainPlayer');
    const downloadBtn = document.getElementById('downloadBtn');
    const videoTitle = document.getElementById('videoTitle');

    if (!inputUrl) return alert("Please paste a link!");

    loading.style.display = "block";
    playerCard.style.display = "none";

    try {
        // Stable Bypasser API
        const response = await fetch(`https://terabox-dl.qtcloud.workers.dev/api/get-info?url=${inputUrl}`);
        const data = await response.json();

        if (data && data.list && data.list.length > 0) {
            const videoData = data.list[0];
            
            // Hum direct link ke bajaye 'dlink' property try karenge jo zyada stable hai
            const streamUrl = videoData.main_url || videoData.dlink;

            videoTitle.innerText = videoData.filename;
            video.src = streamUrl;
            downloadBtn.href = streamUrl;

            loading.style.display = "none";
            playerCard.style.display = "block";
            video.play();
        } else {
            throw new Error("API Limit Reached");
        }
    } catch (error) {
        loading.style.display = "none";
        // Agar worker fail ho jaye toh hum aik auto-redirect link de sakte hain
        alert("Server limit full hai. Is link ko yahan try karein: https://teraboxdownloader.it/");
        window.open(`https://teraboxdownloader.it/?url=${inputUrl}`, '_blank');
    }
});
