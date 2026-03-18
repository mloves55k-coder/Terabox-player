document.getElementById('playBtn').addEventListener('click', async function() {
    const inputUrl = document.getElementById('teralink').value;
    const loading = document.getElementById('loading');
    const playerCard = document.getElementById('player-card');
    const video = document.getElementById('mainPlayer');
    const downloadBtn = document.getElementById('downloadBtn');
    const videoTitle = document.getElementById('videoTitle');

    if (!inputUrl) {
        alert("Please paste a TeraBox link!");
        return;
    }

    // Reset view
    loading.style.display = "block";
    playerCard.style.display = "none";
    video.pause();

    try {
        // Calling the bypasser API used by top bots
        const response = await fetch(`https://terabox-dl.qtcloud.workers.dev/api/get-info?url=${inputUrl}`);
        const data = await response.json();

        if (data.list && data.list.length > 0) {
            const videoData = data.list[0];
            const directUrl = videoData.main_url;

            // Set Title & Video Source
            videoTitle.innerText = videoData.filename || "TeraBox Video";
            video.src = directUrl;
            downloadBtn.href = directUrl;

            // Show Player
            loading.style.display = "none";
            playerCard.style.display = "block";
            video.play();
        } else {
            throw new Error("Invalid response from server");
        }
    } catch (error) {
        loading.style.display = "none";
        alert("Failed to fetch video! This link might be private or broken.");
        console.error("Error:", error);
    }
});
