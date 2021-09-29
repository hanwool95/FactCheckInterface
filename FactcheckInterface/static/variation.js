
$('#claim_button').on('click', function() {
    $('#claim').val('실험중');
})

$('#continue').on('click', function() {
    console.log('click')
    $('#continue_token').val('true');
})

// 출처: https://all-record.tistory.com/172 [세상의 모든 기록]
function changeValue(target, button) {
    console.log('test2');
    var checkBtn = $(button);
    console.log(checkBtn)
    var tr = checkBtn.parent().parent().parent();
    console.log(tr)
    var td = tr.children();
    console.log(td)
    var name = td.eq(1).text().trim();
    console.log(td.eq(1))
    console.log(name);
    document.getElementById(target).value = name;
}



