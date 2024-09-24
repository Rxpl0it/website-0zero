document.addEventListener('DOMContentLoaded', function() {
    const itemType = document.getElementById('item_type');
    const comboFields = document.getElementById('combo_fields');
    const mediaType = document.getElementById('media_type');
    const videoField = document.getElementById('video_field');
    const youtubeField = document.getElementById('youtube_field');

    itemType.addEventListener('change', function() {
        if (this.value === 'combo') {
            comboFields.style.display = 'block';
        } else {
            comboFields.style.display = 'none';
        }
    });

    mediaType.addEventListener('change', function() {
        if (this.value === 'video') {
            videoField.style.display = 'block';
            youtubeField.style.display = 'none';
        } else if (this.value === 'youtube') {
            videoField.style.display = 'none';
            youtubeField.style.display = 'block';
        } else {
            videoField.style.display = 'none';
            youtubeField.style.display = 'none';
        }
    });
});