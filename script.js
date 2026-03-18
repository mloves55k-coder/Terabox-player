document.getElementById('playBtn').addEventListener('click', async function() {
    const inputUrl = document.getElementById('teralink').value.trim();
    const loading = document.getElementById('loading');
    const playerCard = document.getElementById('player-card');
    const video = document.getElementById('mainPlayer');
    const videoTitle = document.getElementById('videoTitle');

    if (!inputUrl) return alert("Please paste a link!");

    loading.style.display = "block";
    playerCard.style.display = "none";

    try {
        // TeraBox link se short ID nikalna
        const urlParts = inputUrl.split('/');
        const shortId = urlParts[urlParts.length - 1].split('?')[0];

        // Alternate Bypasser Link
        const bypassUrl = `https://www.terabox.app/sharing/link?surl=${shortId}`;
        
        // Is link ko play karne ke liye direct stream server use karte hain
        const directStream = `https://terabox-videoplayer.vercel.app/api/parse?url=${inputUrl}`;

        const response = await fetch(directStream);
        const data = await response.json();

        if (data.url) {
            video.src = data.url;
            videoTitle.innerText = data.title || "TeraBox Video";
            loading.style.display = "none";
            playerCard.style.display = "block";
            video.play();
        } else {
            throw new Error("Link not found");
        }
    } catch (error) {
        loading.style.display = "none";
        // Final Fallback: User ko manual link dena
        alert("System busy hai. Ye link try karein: https://teraboxdl.com/");
    }
});
