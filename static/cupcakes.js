const BASE_URL = "http://localhost:5000/api";

function generateCupcakeHTML(cupcake) {
    return `
    <div data-cupcake-id=${cupcake.id}>
        <li>
          ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
          <button class="delete-button btn btn-danger btn-sm">X</button>
        </li>
        <img class="Cupcake-img size"
            src="${cupcake.image}"
            alt="(no image provided)">
    </div>
    `;
}

// Get all cupcakes
async function getCupcakes() {
    const response = await axios.get(`${BASE_URL}/cupcakes`);
    console.log(response.data.cupcakes)

    for (let cupcakeData of response.data.cupcakes) {
        let newCupcake = $(generateCupcakeHTML(cupcakeData));
        $("#cupcakes-list").append(newCupcake);
      }
    }
    
  $("#cupcakes-list").on("click", ".delete-button", async function (evt) {
    evt.preventDefault();
    let $cupcake = $(evt.target).closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");
  
    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
  });


$(getCupcakes);
