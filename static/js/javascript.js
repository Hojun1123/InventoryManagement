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
//달력 한국어 전환
;(function ($) {
    $.fn.datepicker.dates['kr'] = {
        days: ["일요일", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"],
        daysShort: ["일", "월", "화", "수", "목", "금", "토", "일"],
        daysMin: ["일", "월", "화", "수", "목", "금", "토", "일"],
        months: ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"],
        monthsShort: ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"]
    };
}(jQuery));


//달력 날짜 유효성 검사
function CheckReportDate() {
    var startDate = document.getElementById("startDatepicker-report");
    var endDate = document.getElementById("endDatepicker-report");

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
    var startDate2 = document.getElementById("startDatepicker-report").value;
    var endDate2 = document.getElementById("endDatepicker-report").value;

    if (Number(startDate2.replace(/-/gi, "")) > Number(endDate2.replace(/-/gi, ""))) {
        alert("시작일이 종료일보다 클 수 없습니다.");
        startDate.select();
        startDate.focus();
        return false;
    }
    return true;
}

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

    if (Number(startDate2.replace(/-/gi, "")) > Number(endDate2.replace(/-/gi, ""))) {
        alert("시작일이 종료일보다 클 수 없습니다.");
        startDate.select();
        startDate.focus();
        return false;
    }
    return true;
}

//테이블 dropdown 선택 조회
// Get unique values for the desired columns
// {2 : ["M", "F"], 3 : ["RnD", "Engineering", "Design"], 4 : [], 5 : []}
function getUniqueValuesFromColumn() {

    var unique_col_values_dict = {}

    allFilters = document.querySelectorAll(".table-filter")
    allFilters.forEach((filter_i) => {
        col_index = filter_i.parentElement.getAttribute("col-index");
        // alert(col_index)
        const rows = document.querySelectorAll("#filter > tbody > tr")

        rows.forEach((row) => {
            cell_value = row.querySelector("td:nth-child(" + col_index + ")").innerHTML;
            // if the col index is already present in the dict
            if (col_index in unique_col_values_dict) {

                // if the cell value is already present in the array
                if (unique_col_values_dict[col_index].includes(cell_value)) {
                    // alert(cell_value + " is already present in the array : " + unique_col_values_dict[col_index])

                } else {
                    unique_col_values_dict[col_index].push(cell_value)
                    // alert("Array after adding the cell value : " + unique_col_values_dict[col_index])

                }
            } else {
                unique_col_values_dict[col_index] = new Array(cell_value)
            }
        });
    });
    for (i in unique_col_values_dict) {
        //  alert("Column index : " + i + " has Unique values : \n" + unique_col_values_dict[i]);
    }
    updateSelectOptions(unique_col_values_dict)

};

// Add <option> tags to the desired columns based on the unique values

function updateSelectOptions(unique_col_values_dict) {
    allFilters = document.querySelectorAll(".table-filter")

    allFilters.forEach((filter_i) => {
        col_index = filter_i.parentElement.getAttribute('col-index')

        unique_col_values_dict[col_index].forEach((i) => {
            filter_i.innerHTML = filter_i.innerHTML + `\n<option value="${i}">${i}</option>`
        });

    });
};


// Create filter_rows() function
// filter_value_dict {2 : Value selected, 4:value, 5: value}
function filter_rows() {
    allFilters = document.querySelectorAll(".table-filter")
    var filter_value_dict = {}

    allFilters.forEach((filter_i) => {
        col_index = filter_i.parentElement.getAttribute('col-index')

        value = filter_i.value
        if (value != "all") {
            filter_value_dict[col_index] = value;
        }
    });

    var col_cell_value_dict = {};

    const rows = document.querySelectorAll("#filter tbody tr");
    rows.forEach((row) => {
        var display_row = true;

        allFilters.forEach((filter_i) => {
            col_index = filter_i.parentElement.getAttribute('col-index')
            col_cell_value_dict[col_index] = row.querySelector("td:nth-child(" + col_index + ")").innerHTML
        })

        for (var col_i in filter_value_dict) {
            filter_value = filter_value_dict[col_i]
            row_cell_value = col_cell_value_dict[col_i]

            if (row_cell_value.indexOf(filter_value) == -1 && filter_value != "all") {
                display_row = false;
                break;
            }
        }
        if (display_row == true) {
            row.style.display = "table-row"

        } else {
            row.style.display = "none"
        }
    })
}



