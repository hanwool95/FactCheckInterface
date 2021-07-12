// 출처: https://codepen.io/blake_green/pen/VyXXQY

var global_state = 0;
var req_num_row=10;
var count = 0;

// 검색기능 https://wikidocs.net/71806
$(document).ready(function(){

    $("#btn_search").on('click', function() {
        $("#kw").val($(".kw").val());
        $("#kinds_target").val($("#kinds").val());
        $("#searchForm").submit();
    });
});


function make_peg(num_pages){
    // 이전 단추가 첫 페이지에서 생성 안되게 만듦.
    jQuery('.pagination').append("<li><a class=\"begin\"><b>처음으로</b></a></li>");

    if(global_state != 0){
        jQuery('.pagination').append("<li><a class=\"prev\">이전</a></li>");
      }

    for(var i=1; i<=num_pages; i++){
        var state = global_state + i
        if(i === 1){
            jQuery('.pagination').append("<li class='active' id='first'>&nbsp;<a>"+state+"</a></li>");
        }
        else{
            jQuery('.pagination').append("<li>&nbsp;<a>"+state+"</a></li>");
        }
        jQuery('.pagination a').addClass("pagination-link");
        }

    if(global_state != parseInt(count / 100)*10) {
        jQuery('.pagination').append("<li><a class=\"next\">다음</a></li>");
    }
    jQuery('.pagination').append("<li><a class=\"last\"><b>끝으로</b></a></li>");


}

function show_table(start){
    jQuery('tbody tr').hide();
    for(var i=0; i< req_num_row; i++){
        jQuery('tbody tr').eq(+start+i).show();}
}

function pagination(){

    var $tr=jQuery('tbody tr');     // 표의 tbody를 불러옴
    var total_num_row=$tr.length - (global_state*10);   // tbody 길이 불러옴
    count = $tr.length

    // page 개수 계산
    var num_pages=0;
    if(total_num_row % req_num_row ==0){
        num_pages=total_num_row / req_num_row;
    }
    if(total_num_row % req_num_row >=1){
        num_pages=total_num_row / req_num_row;
        num_pages++;
        num_pages=Math.floor(num_pages++);
    }

    if (num_pages >= 11){
        num_pages = 10;
    }

    make_peg(num_pages)
  
    $tr.each(function(i){
        jQuery(this).hide();
        if(i+1 <= req_num_row){
            $tr.eq(i).show();
        }
    });
  
    jQuery('.pagination a').click('.pagination-link', function(e){
        e.preventDefault();
        $tr.hide();
        var page=jQuery(this).text();       // 현재 페이지 수
        var temp=page-1;
        var start=temp*req_num_row;

        jQuery('.pagination li').removeClass("active");
        jQuery(this).parent().addClass("active");

        show_table(start);



        });

    $("#first").trigger("click");

    jQuery('.begin').click(function(){
        global_state = 0
        console.log(global_state);
        jQuery('.pagination').empty()
        pagination()
        show_table(global_state*req_num_row);
    });

    jQuery('.prev').click(function(){
        global_state -= 10
        console.log(global_state);
        jQuery('.pagination').empty()
        pagination()
        show_table(global_state*req_num_row);
    });
 
    jQuery('.next').click(function(e){
        global_state += 10
        console.log(global_state);
        jQuery('.pagination').empty();
        pagination();
        show_table(global_state*req_num_row);

    });

    jQuery('.last').click(function(){
        global_state = parseInt($tr.length / 100)*10
        console.log(global_state);
        jQuery('.pagination').empty();
        pagination();
        show_table(global_state*req_num_row);
    });
 
    }



jQuery('document').ready(function(){
    pagination();
  
  jQuery('.pagination li:first-child').addClass("disabled");
  
});