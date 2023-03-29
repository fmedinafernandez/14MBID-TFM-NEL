// JavaScript source code



function inicio_onclick() {
    const sitelogoDiv = document.getElementById('sitelogo');
    const sitedataDiv = document.getElementById('sitedata');
    const resultPre = document.getElementById('json');

    sitelogoDiv.innerHTML = `      <h1>CLINICAL NEL ENGINE</h1>`;
    resultPre.textContent = "";
    sitedataDiv.innerHTML = "";
    callEngine_Application();
}

function new_informes_onclick() {
    const sitelogoDiv = document.getElementById('sitelogo');
    const sitedataDiv = document.getElementById('sitedata');
    const resultPre = document.getElementById("json");
    sitelogoDiv.innerHTML = `      <h1>CLINICAL NEL ENGINE</h1>

        <form>
        <table style="color: white;">
        <tbody>
        <tr>
        <td><label>Id.Informe</label></td>
        <td><input type="text" id="report_id" name="report_id"></td>
        </tr>
        <tr>
        <td><label>Cuerpo</label></td>
        <td><textarea id="report_input" name="w3review" rows="15" cols="80">
  
          </textarea></td>
        </tr>
        </tbody>
        </table>
          <button type="button" onclick="callEngine_newreport()">
            Enviar Informe
          </button>
        </form>`;

    resultPre.textContent = "";
    sitedataDiv.innerHTML = "";

}


function query_informes_onclick() {
    const sitelogoDiv = document.getElementById('sitelogo');
    const sitedataDiv = document.getElementById('sitedata');
    const resultPre = document.getElementById("json");

    sitelogoDiv.innerHTML = `      <h1>CLINICAL NEL ENGINE</h1>
        Informes
        <form>
          <label>Id informe</label>
          <input type="text" id="idreport" name="idreport">
          <label>Propietario</label>
          <input type="text" id="reportowner" name="reportowner">
          <label for="terminos_clinicos">T\u00e9rmino cl\u00ednico</label>
          <input type="text" id="terminoclinico" name="terminoclinico">
        <button type="button" onclick="callEngine_queryreports()">
          Buscar Informes
        </button>
      </form>`;


    resultPre.textContent = "";
    sitedataDiv.innerHTML = "";
}

function new_termin_onclick() {
    const sitelogoDiv = document.getElementById('sitelogo');
    const sitedataDiv = document.getElementById('sitedata');
    const resultPre = document.getElementById("json");

    sitelogoDiv.innerHTML = `      <h1>CLINICAL NEL ENGINE</h1>
        Nuevo T\u00e9rmino cl\u00ednico
        <form>
          <label>C\u00f3digo t\u00e9rmino</label>
          <input type="text" id="idtermino" name="idtermino">
          <label>T\u00e9rmino</label>
          <input type="text" id="termino" name="termino">
        <button type="button" onclick="callEngine_newtermin()">
          Crear T\u00e9rmino
        </button>
      </form>
  `;


    resultPre.textContent = "";
    sitedataDiv.innerHTML = "";
}

function query_terminos_onclick() {
    const sitelogoDiv = document.getElementById('sitelogo');
    const sitedataDiv = document.getElementById('sitedata');
    const resultPre = document.getElementById("json");

    sitelogoDiv.innerHTML = `    <h1>CLINICAL NEL ENGINE</h1>
      T\u00e9rminos Cl\u00ednicos
      <form>
        <label>C\u00f3digo t\u00e9rmino</label>
        <input type="text" id="idtermino" name="idtermino">
        <label>T\u00e9rmino</label>
        <input type="text" id="termino" name="termino">
      <button type="button" onclick="callEngine_getterminosclinicos(document.getElementById('idtermino').value, document.getElementById('termino').value)">
        Buscar T\u00e9rminos Cl\u00ednicos
      </button>
    </form>
  `;

    resultPre.textContent = "";
    sitedataDiv.innerHTML = "";

}

function update_configuration() {
    const sitelogoDiv = document.getElementById('sitelogo');
    const sitedataDiv = document.getElementById('sitedata');
    const resultPre = document.getElementById("json");

    sitelogoDiv.innerHTML = `    <h1>CLINICAL NEL ENGINE</h1>
      Configuraci\u00f3n
      <form>
        <label>Param 1</label>
        <input type="text" id="param1" name="param1">
      <button type="button" onclick="callEngine_updateconfiguration()">
        Modificar Configuraci\u00f3n
      </button>
    </form>
  `;

    resultPre.textContent = "";
    sitedataDiv.innerHTML = "";

}

function acercade_onclick() {
    const sitelogoDiv = document.getElementById('sitelogo');
    const sitedataDiv = document.getElementById('sitedata');
    const resultPre = document.getElementById("json");

    sitelogoDiv.innerHTML = `      <h1>CLINICAL NEL ENGINE</h1>
      Acerca de...
      <h2>Autor: Fernando Medina Fern\u00e1ndez</h2>
      <h2></h2>
      <table class='sitelogo'>
      <thead><tr><th></th><th></th><th></th></tr></thead>
      <tbody>
      <tr><td></td><td></td><td></td></tr>
      <tr><td></td><td></td><td></td></tr>
      <tr><td></td><td></td><td></td></tr>
      <tr>
      <td>Máster de Big Data y Ciencia de Datos</td>
      <td>Tutor: Igual Pérez, Román</td>
      <td>Primera Convocatoria</td>
      </tr>
      <tr>
      <td>Curso 2022-2023</td>
      <td></td>
      <td>Marzo 2023</td>
      </tr>
      <tr>
      <td></td>
      <td></td>
      <td></td>
      </tr>
      </tbody>
      </table>
      <center><img src='logo-viu.jpg' width='100%' height='auto' display='block'/></center>
  `;

    resultPre.textContent = "";
    sitedataDiv.innerHTML = "";

}
//https://dev.to/vikingcodeblog/4-maneras-de-llamar-a-una-api-rest-con-javascript-2nhm
function callEngine() {

    const sitelogoDiv = document.getElementById('sitelogo');
    const sitedataDiv = document.getElementById('sitedata');
    const resultPre = document.getElementById("json");

    // Creamos un nuevo XMLHttpRequest
    var xhttp = new XMLHttpRequest();

    // Esta es la funci�n que se ejecutar� al finalizar la llamada
    xhttp.onreadystatechange = function () {
        // Si nada da error
        if (this.readyState == 4 && this.status == 200) {
            // La respuesta, aunque sea JSON, viene en formato texto, por lo que tendremos que hace run parse
            result = JSON.parse(this.responseText)
            console.log(result);
            //sitelogoDiv.innerHTML = result
            document.getElementById("json").textContent = JSON.stringify(result, undefined, 2);
        }
    };

    // Endpoint de la API y m�todo que se va a usar para llamar
    xhttp.open("GET", "https://pokeapi.co/api/v2/pokemon", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    // Si quisieramos mandar par�metros a nuestra API, podr�amos hacerlo desde el m�todo send()
    xhttp.send(null);

}

function callEngine_Application() {

  const sitelogoDiv = document.getElementById('sitelogo');
  const sitedataDiv = document.getElementById('sitedata');
  const resultPre = document.getElementById("json");

  // Creamos un nuevo XMLHttpRequest
  var xhttp = new XMLHttpRequest();

  // Esta es la funci�n que se ejecutar� al finalizar la llamada
  xhttp.onreadystatechange = function () {
      // Si nada da error
      if (this.readyState == 4 && this.status == 200) {
          // La respuesta, aunque sea JSON, viene en formato texto, por lo que tendremos que hace run parse
          result = JSON.parse(this.responseText)
          console.log(result);
          //sitelogoDiv.innerHTML = result

          let html = "<table border='1' class='sitedata'>"
          html+="<thead><tr><th>Fecha</th><th>Versi\u00f3n</th></tr></thead>"
          html+="<tbody><tr>"
          html+="<td>" + result.data.date + "</td>"
          html+="<td>" + result.data.version + "</td>"
          html+="</tr></tbody>"
          html += "</table>"

          //document.getElementById("json").textContent = JSON.stringify(result, undefined, 2);
          sitedataDiv.innerHTML = html
      }
  };

  // Endpoint de la API y m�todo que se va a usar para llamar
  xhttp.open("GET", "http://127.0.0.1:5003/application", true);
  //xhttp.setRequestHeader("Content-type", "application/json");
  xhttp.setRequestHeader("user", "usuario");



  // Si quisieramos mandar par�metros a nuestra API, podr�amos hacerlo desde el m�todo send()
  xhttp.send(null);

  sitedataDiv.innerHTML = "<img src='circle-animation.gif' class='sitelogo' width='10%' height='auto' display='block'/>"

}
function callEngine_newreport() {

    const sitelogoDiv = document.getElementById('sitelogo');
    const sitedataDiv = document.getElementById('sitedata');
    const resultPre = document.getElementById("json");
    const report_id = document.getElementById('report_id');
    const report_input = document.getElementById('report_input');
    const hiddentoken = document.getElementById('hiddentoken');
    const token = ""


    //Obtenemos el token
    //callEngine_gettoken();


    // Creamos un nuevo XMLHttpRequest
    var xhttp = new XMLHttpRequest();

    // Esta es la funci�n que se ejecutar� al finalizar la llamada
    xhttp.onreadystatechange = function () {
        // Si nada da error
        if (this.readyState == 4 && this.status == 200) {
            // La respuesta, aunque sea JSON, viene en formato texto, por lo que tendremos que hace run parse
            result = JSON.parse(this.responseText)
            console.log(result);
            //sitelogoDiv.innerHTML = result

            let html = "<table border='1' class='sitedata'>"
            html+="<thead><tr><th>Fuente preprocesada</th><th>T\u00e9rmino</th><th>Distancia/similitud</th></tr></thead><tbody>"
            for (let i = 0; i < result.data.length; i++) {
              html+="<tr>"
              html+="<td>" + result.data[i].source_text + "</td>"
              html+="<td>" + result.data[i].termino + "</td>"
              html+="<td>" + (result.data[i].cosine_similarity * 100) + "%</td>"
              html+="</tr>"
            }
            html += "</tbody></table>"
  
            //document.getElementById("json").textContent = JSON.stringify(result, undefined, 2);
            sitedataDiv.innerHTML = html
  

        }
    };
    //console.log("1")
    // Endpoint de la API y m�todo que se va a usar para llamar
    xhttp.open("PUT", "http://127.0.0.1:5003/reports", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.setRequestHeader("user", "usuario");
    xhttp.setRequestHeader("reportid", report_id.value);
    xhttp.setRequestHeader("token", hiddentoken.value);
    xhttp.setRequestHeader("model", "0");
    // Si quisieramos mandar par�metros a nuestra API, podr�amos hacerlo desde el m�todo send()
    xhttp.send(report_input.value);
    //console.log("2")
    sitedataDiv.innerHTML = "<center><img src='circle-animation.gif' class='sitelogo' display='block'/></center>"


}


function callEngine_getversion() {

    const sitelogoDiv = document.getElementById('sitelogo');
    const sitedataDiv = document.getElementById('sitedata');
    const resultPre = document.getElementById("json");

    // Creamos un nuevo XMLHttpRequest
    var xhttp = new XMLHttpRequest();

    // Esta es la funci�n que se ejecutar� al finalizar la llamada
    xhttp.onreadystatechange = function () {
        // Si nada da error
        if (this.readyState == 4 && this.status == 200) {
            // La respuesta, aunque sea JSON, viene en formato texto, por lo que tendremos que hace run parse
            result = JSON.parse(this.responseText)
            console.log(result);
            //sitelogoDiv.innerHTML = result
            document.getElementById("json").textContent = JSON.stringify(result, undefined, 2);
        }
    };
    // Endpoint de la API y m�todo que se va a usar para llamar
    xhttp.open("GET", "http://127.0.0.1:5003/application", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    // Si quisieramos mandar par�metros a nuestra API, podr�amos hacerlo desde el m�todo send()
    xhttp.send();

    sitedataDiv.innerHTML = "<center><img src='circle-animation.gif' class='sitelogo' display='block'/></center>"

}

function callEngine_gettoken() {

    const sitelogoDiv = document.getElementById('sitelogo');
    const sitedataDiv = document.getElementById('sitedata');
    const resultPre = document.getElementById("json");
    const hiddentoken = document.getElementById('hiddentoken');

    // Creamos un nuevo XMLHttpRequest
    var xhttp = new XMLHttpRequest();

    // Esta es la funci�n que se ejecutar� al finalizar la llamada
    xhttp.onreadystatechange = function () {
        // Si nada da error
        if (this.readyState == 4 && this.status == 200) {
            // La respuesta, aunque sea JSON, viene en formato texto, por lo que tendremos que hace run parse
            result = JSON.parse(this.responseText)
            console.log(result);
            //sitelogoDiv.innerHTML = result
            //json_result = JSON.stringify(result, undefined, 2);
            hiddentoken.value = result.token;
            return result.token;
        }
    };
    // Endpoint de la API y m�todo que se va a usar para llamar
    xhttp.open("GET", "http://127.0.0.1:5003/users", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.setRequestHeader("user", "user");
    xhttp.setRequestHeader("password", "password");
    // Si quisieramos mandar par�metros a nuestra API, podr�amos hacerlo desde el m�todo send()
    xhttp.send();

}

function callEngine_getterminosclinicos(idtermino, termino) {
    console.log(termino);

    const sitelogoDiv = document.getElementById('sitelogo');
    const sitedataDiv = document.getElementById('sitedata');
    const resultPre = document.getElementById("json");
    const hiddentoken = document.getElementById('hiddentoken');

    // Creamos un nuevo XMLHttpRequest
    var xhttp = new XMLHttpRequest();

    // Esta es la funci�n que se ejecutar� al finalizar la llamada
    xhttp.onreadystatechange = function () {
        // Si nada da error
        if (this.readyState == 4 && this.status == 200) {
            // La respuesta, aunque sea JSON, viene en formato texto, por lo que tendremos que hace run parse
            result = JSON.parse(this.responseText)
            console.log(result);
            //sitelogoDiv.innerHTML = result
            //json_result = JSON.stringify(result, undefined, 2);

            //renderizar una tabla con los resultados

            let html = "<table border='1' class='sitedata'>"
            html+="<thead><tr><th>Identificador</th><th>C\u00f3digo</th><th>Descripcion</th></tr></thead><tbody>"
            for (let i = 0; i < result.data.length; i++) {
              html+="<tr>"
              html+="<td>" + result.data[i].id + "</td>"
              html+="<td>" + result.data[i].idtermino + "</td>"
              html+="<td>" + result.data[i].termino + "</td>"
              html+="</tr>"
            }
            html += "</tbody></table>"
  
            //document.getElementById("json").textContent = JSON.stringify(result, undefined, 2);
            sitedataDiv.innerHTML = html


        }
    };
    // Endpoint de la API y m�todo que se va a usar para llamar
    xhttp.open("GET", "http://127.0.0.1:5003/terminosclinicos", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.setRequestHeader("token", hiddentoken.value)
    xhttp.setRequestHeader("user", "usuario");
    if (idtermino != ""){
      xhttp.setRequestHeader("id", idtermino);
    }
    if (termino != ""){
      xhttp.setRequestHeader("termino", termino);
    }
    // Si quisieramos mandar par�metros a nuestra API, podr�amos hacerlo desde el m�todo send()
    xhttp.send();
    sitedataDiv.innerHTML = "<center><img src='circle-animation.gif' class='sitelogo' display='block'/></center>"

}


function callEngine_queryreports() {

    const sitelogoDiv = document.getElementById('sitelogo');
    const sitedataDiv = document.getElementById('sitedata');
    const resultPre = document.getElementById("json");
    const hiddentoken = document.getElementById('hiddentoken');
    const idreport = document.getElementById('idreport');
    const reportowner = document.getElementById('reportowner');
    const terminoclinico = document.getElementById('terminoclinico');

    // Creamos un nuevo XMLHttpRequest
    var xhttp = new XMLHttpRequest();

    // Esta es la funci�n que se ejecutar� al finalizar la llamada
    xhttp.onreadystatechange = function () {
        // Si nada da error
        if (this.readyState == 4 && this.status == 200) {
            // La respuesta, aunque sea JSON, viene en formato texto, por lo que tendremos que hace run parse
            result = JSON.parse(this.responseText)
            console.log(result);
            //sitelogoDiv.innerHTML = result
            //json_result = JSON.stringify(result, undefined, 2);

            //renderizar una tabla con los resultados

            let html = "<table border='1' class='sitedata'>"
            html+="<thead><tr><th>Identificador</th><th>Usuario</th><th>Cuerpo</th><th>Etiquetas</th></tr></thead><tbody>"
            idreport_ant = '';
            reportbody_ant = '';
            for (let i = 0; i < result.data.length; i++) {
              if(reportbody_ant != result.data[i].reportbody || idreport_ant != result.data[i].idreport){
                if(reportbody_ant != ''){
                  html+="</tbody></table></td>"
                  html+="</tr>"
                }
                idreport_ant = result.data[i].idreport;
                reportbody_ant = result.data[i].reportbody;
                html+="<tr>"
                html+="<td>" + result.data[i].idreport + "</td>"
                html+="<td>" + result.data[i].owner + "</td>"
                html+="<td>" + result.data[i].reportbody + "</td>"
                html+="<td><table border='1' class='sitedata'><thead><tr><th>Fuente preprocesada</th><th>T\u00e9rmino</th><th>Distancia/similitud</th></tr></thead><tbody>"
                html+="<tr>"
                html+="<td>" + result.data[i].source_text + "</td>"
                html+="<td>" + result.data[i].termino + "</td>"
                html+="<td>" + ('' + (result.data[i].cosine_similarity * 100)).substring(0,5) + "%</td>"
                html+="</tr>"
              }else{
                html+="<tr>"
                html+="<td>" + result.data[i].source_text + "</td>"
                html+="<td>" + result.data[i].termino + "</td>"
                html+="<td>" + ('' + (result.data[i].cosine_similarity * 100)).substring(0,5) + "%</td>"
                html+="</tr>"
              }
            }
            html += "</tbody></table>"
  
            //document.getElementById("json").textContent = JSON.stringify(result, undefined, 2);
            sitedataDiv.innerHTML = html

        }
    };
    // Endpoint de la API y m�todo que se va a usar para llamar
    xhttp.open("GET", "http://127.0.0.1:5003/reports", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.setRequestHeader("user", "usuario")
    xhttp.setRequestHeader("token", hiddentoken.value)
    xhttp.setRequestHeader("idreport", idreport.value)
    xhttp.setRequestHeader("owner", reportowner.value)
    xhttp.setRequestHeader("termino", terminoclinico.value)
    // Si quisieramos mandar par�metros a nuestra API, podr�amos hacerlo desde el m�todo send()
    xhttp.send();
    sitedataDiv.innerHTML = "<center><img src='circle-animation.gif' class='sitelogo' display='block'/></center>"

}

function callEngine_newtermin() {

    const sitelogoDiv = document.getElementById('sitelogo');
    const sitedataDiv = document.getElementById('sitedata');
    const resultPre = document.getElementById("json");
    const hiddentoken = document.getElementById('hiddentoken');
    const idtermino = document.getElementById('idtermino');
    const termino = document.getElementById('termino');

    // Creamos un nuevo XMLHttpRequest
    var xhttp = new XMLHttpRequest();

    // Esta es la funci�n que se ejecutar� al finalizar la llamada
    xhttp.onreadystatechange = function () {
        // Si nada da error
        if (this.readyState == 4 && this.status == 200) {
            // La respuesta, aunque sea JSON, viene en formato texto, por lo que tendremos que hace run parse
            result = JSON.parse(this.responseText)
            console.log(result);
            //sitelogoDiv.innerHTML = result
            //document.getElementById("json").textContent = JSON.stringify(result, undefined, 2);

            let html = "<table border='1' class='sitedata'>"
            html+="<thead><tr><th>Identificador</th><th>C\u00f3digo</th><th>Descripcion</th></tr></thead><tbody>"
              html+="<tr>"
              html+="<td>" + result.result[0].id + "</td>"
              html+="<td>" + result.result[0].idtermino + "</td>"
              html+="<td>" + result.result[0].termino + "</td>"
              html+="</tr>"
            html += "</tbody></table>"
  
            //document.getElementById("json").textContent = JSON.stringify(result, undefined, 2);
            sitedataDiv.innerHTML = html



        }
    };
    // Endpoint de la API y m�todo que se va a usar para llamar
    xhttp.open("PUT", "http://127.0.0.1:5003/terminosclinicos", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.setRequestHeader("user", "usuario")
    xhttp.setRequestHeader("token", hiddentoken.value)
    xhttp.setRequestHeader("idtermino", idtermino.value)
    xhttp.setRequestHeader("termino", termino.value)
    // Si quisieramos mandar par�metros a nuestra API, podr�amos hacerlo desde el m�todo send()
    xhttp.send();
    sitedataDiv.innerHTML = "<center><img src='circle-animation.gif' class='sitelogo' display='block'/></center>"

}

function callEngine_updateconfiguration() {

    const sitelogoDiv = document.getElementById('sitelogo');
    const sitedataDiv = document.getElementById('sitedata');
    const resultPre = document.getElementById("json");
    const hiddentoken = document.getElementById('hiddentoken');
    const param1 = document.getElementById('param1');

    // Creamos un nuevo XMLHttpRequest
    var xhttp = new XMLHttpRequest();

    // Esta es la funci�n que se ejecutar� al finalizar la llamada
    xhttp.onreadystatechange = function () {
        // Si nada da error
        if (this.readyState == 4 && this.status == 200) {
            // La respuesta, aunque sea JSON, viene en formato texto, por lo que tendremos que hace run parse
            result = JSON.parse(this.responseText)
            console.log(result);
            //sitelogoDiv.innerHTML = result
            document.getElementById("json").textContent = JSON.stringify(result, undefined, 2);
        }
    };
    // Endpoint de la API y m�todo que se va a usar para llamar
    xhttp.open("PUT", "http://127.0.0.1:5003/terminosclinicos", true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.setRequestHeader("token", hiddentoken.value)
    xhttp.setRequestHeader("param1", param1.value)
    // Si quisieramos mandar par�metros a nuestra API, podr�amos hacerlo desde el m�todo send()
    xhttp.send(report_input.value);
    sitedataDiv.innerHTML = "<center><img src='circle-animation.gif' class='sitelogo' display='block'/></center>"

}
