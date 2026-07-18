setInterval(() => {
    const player = document.querySelector("#movie_player");

    if (player && typeof player.getVideoData === "function") {
        const id = player.getVideoData().video_id;

        window.postMessage({
            type: "YT_VIDEO_ID",
            id: id
        }, "*");
    }
}, 500);