// noinspection BadExpressionStatementJS
console.log("connected")
new tempusDominus.TempusDominus(document.getElementById('example'), {

    // options here

});


/*$.get('/home/doleanceencours', function (response) {
    const data = response.data
    //console.log('test', data)
    data.forEach((item) => {
        console.log(item.ndi.split('/'))
    })

})*/

/*
$(document).ready(function () {

*/

/*
$('#demandeencours').DataTable({
    'ajax': {
        "type": "GET",
        "url": "home/doleanceencours"
    },
    'columns': [
        {'data': "ndi"},
        {'data': 'date_transmission'},
        {'data': "statut"},
        {'data': "station.libelle_station"},
        {'data': 'element'},
        {'data': 'panne_declarer'},
        {'data': 'date_deadline'},
        {'data': 'commentaire'},
    ],
    pageLength: 10,
    order: true,
    'columnDefs': [{
        "targets": 0,
        "data": "ndi",
        "textAlign": "right",
        "render": function (data) {
            return `
                <a href="#" id="ndi" style="text-transform: uppercase">${data}</a>
                `
        },
    }],

})
*/


/*
$.ajax({
    url: '/home/doleanceAll',
    type: 'GET',
    success: function (response) {
        let data = response.data
        data.forEach(element => {
            //console.log(element.ndi.split("/"))
        })

    },
    error: function (error) {
        console.log(error)
    }
})
const ndiEvent = document.getElementById('ndi')
// console.log('klkl', ndiEvent)
// ndiEvent.onclick(function () {
//     console.log('cliked')
// })

$.ajax({
    url: `/home/personnel/1`,
    type: 'GET',
    success: function (response) {
        let data = response.data

        console.log(data.nom_personnel)
    },
    error: function (error) {
        console.log(error)
    }
})
$.get('/home/personnel/1', function (data) {
    console.log('test', data)
})*/
