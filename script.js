document.getElementById('playBtn').addEventListener('click', async function() {
    const inputUrl = document.getElementById('teralink').value.trim();
    const loading = document.getElementById('loading');
    const playerCard = document.getElementById('player-card');
    const video = document.getElementById('mainPlayer');
    const downloadBtn = document.getElementById('downloadBtn');
    const videoTitle = document.getElementById('videoTitle');

    if (!inputUrl) {
        alert("Please paste a TeraBox link!");
        return;
    }

    loading.style.display = "block";
    playerCard.style.display = "none";

    // Hum direct workers.dev ke bajaye ek powerful bypasser use karenge
    const apiEndpoint = `https://terabox-dl.qtcloud.workers.dev/api/get-info?url=${inputUrl}`;
    
    // Proxy use kar rahe hain taake browser block na kare (CORS fix)
    const proxyUrl = 'https://api.allorigins.win/get?url=' + encodeURIComponent(apiEndpoint);

    try {
        const response = await fetch(proxyUrl);
        const proxyData = await response.json();
        
        // allorigins data ko JSON mein parse karta hai
        const data = JSON.parse(proxyData.contents);

        if (data && data.list && data.list.length > 0) {
            const videoData = data.list[0];
            
            // Link ko format karna
            let finalLink = videoData.main_url;
            
            videoTitle.innerText = videoData.filename || "TeraBox Video";
            video.src = finalLink;
            downloadBtn.href = finalLink;

            loading.style.display = "none";
            playerCard.style.display = "block";
            
            // Auto play koshish
            video.play().catch(() => console.log("Auto-play blocked by browser"));
        } else {
            throw new Error("Invalid Link");
        }
    } catch (error) {
        loading.style.display = "none";
        alert("Server Busy! Is link ko 2-3 baar try karein ya browser refresh karein.");
        console.error("Error details:", error);
    }
});
