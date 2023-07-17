const BASE_URL = "http://localhost:5000/api";

// Generate HTML for a cupcake
function generateCupcakeHTML(cupcake) {
 return` <div id="cupcake-card" class="card mb-3" data-cupcake-id=${cupcake.id}>
  <h3 class="card-header">${cupcake.flavor} Cupcake</h3>
  <div class="card-body">
    <h5 class="card-title">${cupcake.size}</h5>
    <h6 class="card-subtitle text-muted">${cupcake.rating}</h6>
  </div>
  <img src="${cupcake.image}" class="d-block user-select-none" aria-label="Placeholder: Image cap" focusable="false"  preserveAspectRatio="xMidYMid slice" viewBox="0 0 318 180" style="font-size:1.125rem;text-anchor:middle">
    <text x="50%" y="50%" fill="#dee2e6" dy=".3em">Image cap</text>
  </img>
 
 <div class="card-body">
    <a href="#" class="card-link">Card link</a>
    <a href="#" class="card-link">Another link</a>
  </div>
  <button class="delete-button btn btn-danger btn-sm">X</button>
</div>
`;
}

// Get all cupcakes and append to list
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


// Initialize all Cupcakes
$(getCupcakes);



 // return `
    // <div data-cupcake-id=${cupcake.id}>
    //     <li>
    //       ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
    //       <button class="delete-button btn btn-danger btn-sm">X</button>
    //     </li>
    //     <img class="Cupcake-img size"
    //         src="${cupcake.image}"
    //         alt="(no image provided)">
    // </div>
    // `;