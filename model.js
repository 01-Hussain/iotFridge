const axios = require('axios');
const fs = require('fs');
function get_images() {
    function get_image(image_name, folder) {
        let url = 'http://192.168.100.200/capture';
        axios.get(url, { responseType: 'arraybuffer' })
            .then(response => {
                fs.writeFileSync(`images/${folder}/${image_name}.jpg`, Buffer.from(response.data, 'binary'));
            });
    }

    function processImages(folder) {
        let i = 1;
        const totalIterations = 10;

        function processNextImage() {
            if (i <= totalIterations) {
                get_image(`${i}`, folder);
                i++;

                setTimeout(processNextImage, 500);
            }
        }

        processNextImage();
    }


    processImages('train');

    setTimeout(() => {
        processImages('val');
    }, 3000);
}
exports.get_images = get_images;