function consulta_ajax(datos) {
  const tabla = document.getElementById("tabla-cotizaciones");
  const tbody = tabla.getElementsByTagName("tbody")[0];
  tbody.innerHTML = ""; // Limpia el contenido actual del tbody

  for (const dato of datos) {
    
    const fila = tbody.insertRow(-1);
    fila.id = dato.ticker;

    const celda1 = fila.insertCell(0);
    celda1.innerHTML = dato.ticker;

    const celda2 = fila.insertCell(1);
    celda2.innerHTML = dato.last;

    const celda3 = fila.insertCell(2);
    celda3.innerHTML = dato.bid[0].price;
   
    const celda4 = fila.insertCell(3);
    celda4.innerHTML = dato.bid[0].size;

    const celda5 = fila.insertCell(4);
    celda5.innerHTML = dato.offer[0].price;

    const celda6 = fila.insertCell(5);
    celda6.innerHTML = dato.offer[0].size;

  }
}
    // Llamada directa a la función consulta_ajax()
  //  consulta_ajax();
  
   

//function actualizarTabla(datos) {
 
  //  for (ticker in datos) {
  //    const cotizacion = datos[ticker];
 //     const fila = $('#tabla-cotizaciones #' + ticker);
  //      console.log("___________________________",ticker);
 //     
 //     if (fila.length == 0) {
 //       // Si no existe la fila, la agregamos
 //       $('#tabla-cotizaciones tbody').append(`
 //         <tr id="${ticker}">
 //           <td>${ticker}</td>
 //           <td>${cotizacion.last}</td>
 //           <td>${cotizacion.bid_price}</td>
 //           <td>${cotizacion.ask_price}</td>
 //         </tr>
 //       `);
 //     } else {
        // Si ya existe la fila, actualizamos los datos
//        fila.find('td:nth-child(2)').text(cotizacion.last);
//        fila.find('td:nth-child(3)').text(cotizacion.bid_price);
//        fila.find('td:nth-child(4)').text(cotizacion.ask_price);
//      }
 //   }
 // }

  // Código para conectarse al servidor WebSocket y recibir las actualizaciones
  // Utiliza la función "actualizarTabla" para actualizar la tabla en tiempo real