$(document).ready(function () {

    let ctx1 = document.getElementById('myChart-1').getContext('2d');
    let ctx2 = document.getElementById('myChart-2').getContext('2d');
    let ctx3 = document.getElementById('myChart-3').getContext('2d');
    var departments = [];

    $.ajax({

        url: "/graphs/",
        dataType: "json"

    }).done(function (data) {

        if (data) {

            let departments = data['departments']
            let skills = data["skills"]
            let tickets = data['tickets']
            let users = data['users']

            console.log(users)


            let chart1Data = []
            let chart2Data = []
            let chart3Data = []

            for(i=0;i<departments.length;i++) {

                let data = {
                    departName: '',
                    ticketCount: 0,
                }

                data.departName = departments[i]['department_name']

                for(j=0;j<tickets.length;j++) {

                    if (tickets[j]['user_department'] == departments[i]['id']) {

                        data.ticketCount += 1;
                    }

                }

                chart3Data.push(data)
            }

            for (i=0;i<skills.length;i++) {
                let data = {
                    requestType: "",
                    ticketCount: 0,
                }
                data.requestType = skills[i]["skill_type"]
                for (j=0;j<tickets.length;j++) {
                    if (tickets[j]['request_type'] == skills[i]['id']) {
                        data.ticketCount += 1;
                    }
                }
                chart2Data.push(data)
            }

            for (i=0;i<users.length;i++) {
                let data = {
                    user: "",
                    ticketCount: 0,
                }
                data.user = users[i]['first_name']
                for (j=0;j<tickets.length;j++) {
                    if (tickets[j]['staff_assigned'] == users[i]['id']) {
                        data.ticketCount += 1;
                    }
                }
                chart1Data.push(data)
            }

            let myChart1 = new Chart(ctx1, {

                type: 'horizontalBar',

                data: {
                    labels: chart1Data.map((obj) => {return obj.user}),
                    datasets: [{
                        label: 'Number of Tickets by Technician',
                        data: chart1Data.map((obj) => {return obj.ticketCount}),
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderwidth: 1
                    }],
                    fill: false,
                },
            })
            let myChart2 = new Chart(ctx2, {

                type: 'pie',

                data: {
                    labels: chart2Data.map((obj) => {return obj.requestType}),
                    datasets: [{
                        label: 'Tickets by Request Type',
                        data: chart2Data.map((obj) => {return obj.ticketCount}),
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)',
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(54, 162, 235, 1)',
                        ],
                        borderwidth: 1
                    }]
                },

            })
            let myChart3 = new Chart(ctx3, {

                type: 'bar',

                data: {
                    labels: chart3Data.map(function (obj) {return obj.departName}),
                    datasets: [{
                        label: 'Tickets by Department',
                        data: chart3Data.map(function(obj) {return obj.ticketCount}),
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderwidth: 1
                    }]
                },
            })


        }

     })






})