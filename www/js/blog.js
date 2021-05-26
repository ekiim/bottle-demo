///
// URI
// - schema://netloc/path/to/route?query=params&search=param
//  schema: protocolo
//  netloc: es maquina, puerto, y usuario.
//  /path/to/route : es el PATH o Ruta , Default: /
//  ?: campo de busqueda
// ---
// HTTP
//      GET
//      POST
//      PUT
//      PATCH
//      DELETE
//      OPTIONS
//
// GET URI, HEADERS, BODY

window.addEventListener("load", async (e) => {
    console.log("Soy blog JS");

    const blogEntryName = document.getElementById("blog-entry-name").value;
    console.log(`Estamos en la entrada de blog ${blogEntryName}`);

    var API_URL = "http://0.0.0.0:9999";
    var route = `/comments/${blogEntryName}`
    const comments_api_url = `${API_URL}${route}`

    const comments_request = await fetch(comments_api_url, {
        method: "GET",
        mode: "cors",
    });
    const comments_data = await comments_request.json()
    console.log(comments_request);
    console.log(comments_data);
    const feedId = "comment-feed";
    w3.displayObject(feedId, comments_data);

});
