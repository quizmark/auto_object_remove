function calcRate(r) {
    $.ajax({type: "POST",
        url:'create-model/',     
        data: {csrfmiddlewaretoken: "{{ csrf_token }}",value: r},
        success:  function(response){alert(response);}
    });
    //const f = ~~r;//Tương tự Math.floor(r)
    // id = 'star' + f + (r % f !=0 ? 'half' : '');
    //alert(r);
    // if(document.getElementById(id).checked = !0)
    // {
                
    // }
}

