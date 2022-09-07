/* --------------------------
SCRIPTS PARA TODA LA PAGINA
-----------------------------*/

// 1) funcion cuando pulsa el texto
$(document).ready(function(){
    (function pulse() {
        $('.text-pulse').fadeOut(1000).fadeIn(1000, pulse);

    })();
})

//2) Funcion para mostrar la contraseña
function myFunction(params) {
    let p = document.getElementById("password")
    if(p.type === "password"){
        p.type = 'text';
    }else{
        p.type = 'password';
    }
}

// 3) Contador de caracteres
$(document).ready(function(){
    let start = 0;
    let limit = 1000;

    $('#message').keyup(function(){
        start = this.value.length
        if (start > limit){
            return false
        }
        else if (start == 1000){
            $('#remaining').html("Numero de caracteres: " + (limit - start)).css('color','red');
            swal("Opss", "Limite de caracteres", "info")
        }
        else if (start > 984){
            $('#remaining').html("Numero de caracteres: " + (limit - start)).css('color','red');
        }
        else if (start < 1000){
            $('#remaining').html("Numero de caracteres: " + (limit - start)).css('color','black');
        }
        else{
            $('#remaining').html("Numero de caracteres: " + (limit)).css('color','black');
        }
    })
})

// 4) InputMask Para numero de celular
$(document).ready(function(){
    $(".phone").inputmask("(00) 999-999-9999", {"onincomplete": function(){
        swal("Opss", "Falta el numero", "info");
        $(".phone").val("");
        return false;
    }})
})

// 5) script para aceptar archivos menores a 2mb
$(document).ready(function(){
    let upload = document.getElementById("file");
    upload.onchange = function(){
        if(this.files[0].size > 2 * 1048576){
            swal("Atencion", "Maximo solo 2mb", "info");
            this.value = ""
        };
    };
});

// 6) Script para cerrar menu hamburgusa automatico
$(document).ready(function(){
    jQuery("#offcanvasRight, .offcanvas-body a").click(function(){
        console.log($(this).attr("href"))
        jQuery('.offcanvas').offcanvas('hide');
    });
})

// 7) Script para cuando no encuntre mensajes en el buscador
$(document).ready(function(){
    let verify = $('#chk_td').length;
    if (verify == 0) {
        $(".hide").css('display', 'none')
        $("#msg").text("No se encontraron registros")
        $("#refresh").html('<i class="fas fa-sync-alt fa-3x"></i>')
    }
})