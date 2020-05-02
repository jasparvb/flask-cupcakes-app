const BASE_URL = "http://127.0.0.1:5000/api";

class fetchAllCupcakes {
    constructor() {
        this.getCupcakes()
    }

    async getCupcakes() {
        const response = await axios.get(`${BASE_URL}/cupcakes`);
        console.log(response);
        for(let cupcake of response.data.cupcakes) {
            this.generateHTML(cupcake);
        }
    }
    
    generateHTML(cupcake) {
        let $item = $(`
            <li>
                <img class="" src="${cupcake.image}">
                <p>Flavor: ${cupcake.flavor}<br>
                Size: ${cupcake.size}<br>
                Rating: ${cupcake.rating}</p>
                <button data-id="${cupcake.id}">Delete</button>
            </li>
        `);
        $('#cupcake-list').append($item);
    }
}

class createCupcakes {
    constructor() {
        $('#add-cupcake-form').on('submit', this.addCupcake.bind(this))
    }

    async addCupcake(e) {
        e.preventDefault();
        console.log('submitted');
        let flavor = $('#flavor').val();
        let size = $('#size').val();
        let rating = $('#rating').val();
        let image = $('#iamge').val();
        const response = await axios.post(`${BASE_URL}/cupcakes`, {flavor, size, rating, image});
        console.log(response);
    }
}

$(async function() {
    new fetchAllCupcakes();
    new createCupcakes();
});