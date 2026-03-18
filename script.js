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

    // Koshish 1: Primary API
    try {
        const response = await fetch(`https://terabox-dl.qtcloud.workers.dev/api/get-info?url=${inputUrl}`);
        const data = await response.json();

        if (data.list && data.list.length > 0) {
            showVideo(data.list[0]);
        } else {
            // Agar pehli fail ho jaye, toh Koshish 2: Alternate API
            const altResponse = await fetch(`https://terabox-api.herokuapp.com/api/info?url=${inputUrl}`);
            const altData = await altResponse.json();
            
            if(altData.direct_link) {
                showVideo({
                    main_url: altData.direct_link,
                    filename: altData.file_name
                });
            } else {
                throw new Error("All APIs failed");
            }
        }
    } catch (error) {
        loading.style.display = "none";
        alert("API Busy hai ya link expire ho gaya hai. Dobara koshish karein ya koi aur link try karein.");
    }

    function showVideo(videoData) {
        videoTitle.innerText = videoData.filename || "TeraBox Video";
        video.src = videoData.main_url;
        downloadBtn.href = videoData.main_url;
        loading.style.display = "none";
        playerCard.style.display = "block";
        video.play();
    }
});
