window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

;(function ($) {
    $.fn.datepicker.dates['kr'] = {
        days: ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"],
        daysShort: ["일", "월", "화", "수", "목", "금", "토", "일"],
        daysMin: ["일", "월", "화", "수", "목", "금", "토", "일"],
        months: ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"],
        monthsShort: ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]
    };
}(jQuery));

function CheckDate() {
    var startDate = document.getElementById("startDatepicker");
    var endDate = document.getElementById("endDatepicker");

    if (startDate.value === "") {
        alert("시작 날짜를 정해주세요.");
        startDate.select();
        startDate.focus();
        return false;
    } else if (endDate.value === "") {
        alert("마지막 날짜를 선택해주세요.");
        endDate.select();
        endDate.focus();
        return false;
    }
    var startDate2 = document.getElementById("startDatepicker").value;
    var endDate2 = document.getElementById("endDatepicker").value;

    if( Number(startDate2.replace(/-/gi,"")) > Number(endDate2.replace(/-/gi,"")) ){
        alert("시작일이 종료일보다 클 수 없습니다.");
        startDate.select();
        startDate.focus();
        return false;
    }
    return true;
}
