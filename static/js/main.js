

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner(0);


    // Fixed Navbar
    $(window).scroll(function () {
        if ($(window).width() < 992) {
            if ($(this).scrollTop() > 55) {
                $('.fixed-top').addClass('shadow');
            } else {
                $('.fixed-top').removeClass('shadow');
            }
        } else {
            if ($(this).scrollTop() > 55) {
                $('.fixed-top').addClass('shadow').css('top', -55);
            } else {
                $('.fixed-top').removeClass('shadow').css('top', 0);
            }
        } 
    });
    
    
   // Back to top button
   $(window).scroll(function () {
    if ($(this).scrollTop() > 300) {
        $('.back-to-top').fadeIn('slow');
    } else {
        $('.back-to-top').fadeOut('slow');
    }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Testimonial carousel
 


    // Modal Video
    $(document).ready(function () {
        var $videoSrc;
        $('.btn-play').click(function () {
            $videoSrc = $(this).data("src");
        });
        console.log($videoSrc);

        $('#videoModal').on('shown.bs.modal', function (e) {
            $("#video").attr('src', $videoSrc + "?autoplay=1&amp;modestbranding=1&amp;showinfo=0");
        })

        $('#videoModal').on('hide.bs.modal', function (e) {
            $("#video").attr('src', $videoSrc);
        })
    });



    // Product Quantity
    $('.quantity').on('click', function () {
        var button = $(this);
        var oldValue = button.parent().parent().find('input').val();
        if (button.hasClass('btn-plus')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        button.parent().parent().find('input').val(newVal);
    });





    
    $('.plus-cart').click(function(){
        var id=$(this).attr("pid").toString();
        var eml=this.parentNode.children[1]
      
       
        
      
     
        $.ajax({
          type:"GET",
          url:"/pluscart",
          data:{
            prod_id:id
          },
          success:function(data){
            eml.innerText =data.quantity
            document.querySelector(".tamount").innerText=data.totalamount
            document.querySelector(".amount").innerText=data.amount
          }
    
    
    
        })
    
    })
    
    $('.minus-cart').click(function(){
      var id=$(this).attr("pid").toString();
      var eml=this.parentNode.children[1]
     
    
      
    
      $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
          prod_id:id
        },
        success:function(data){
          eml.innerText =data.quantity
          document.querySelector(".amount").innerText=data.amount
          
    
          document.querySelector(".tamount").innerText=data.totalamount
     
       
         
        }
    
    
    
      })
    
    })
    

    
    
$('.remove-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this
  


    
  
    $.ajax({
      type:"GET",
      url:"/removecart",
      data:{
        prod_id:id
      },
      success:function(data){
        document.querySelector(".amount").innerText=data.amount
    
        document.querySelector(".tamount").innerText=data.totalamount
  
        eml.parentNode.parentNode.remove()
   
     
       
      }
  
  
  
    })
  
  })






// ------------cart---
