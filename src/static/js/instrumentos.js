let btn = document.getElementById('btn-guardar_inst');
            btn.addEventListener('click', (e) => {
                // handle the click event
                alert("fdlafsag");
                console.log('clicked');
            });

  //no está llamada en ningun lado este instrumentos.js           
let fechaGuardada = localStorage.getItem("date")
      let now = new Date()
      now = now.getDate() +" "+now.getMonth() +" "+now.getYear();
      
      let date1 = new Date(now);
      let date2 = new Date(fechaGuardada);
      console.log(date1.getTime())
      console.log(date2.getTime())
      if (date1.getTime() < date2.getTime()){
        console.log("if entra y guarda fecha y token")
      }else{
        console.log("las fechas son iguales")
     }
           
           token = document.getElementsByName("tokens")[0].value;
           let fecha = new Date()
           fecha = fecha.getDate() +" "+fecha.getMonth() +" "+fecha.getYear();
           console.log(fecha)
           localStorage.setItem('token', token);
           localStorage.setItem('date', fecha);
