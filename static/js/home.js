const clientSelect = document.getElementById('id_client_id')
console.log(clientSelect)
$.ajax({
    type: 'GET',
    url: '/get-client/',
    success: function (response) {
        const clientData = response.client
        console.log(clientData)
  //  === UTLISATION DE CRISPY FORM ET BOOTSTRAP AJAX ===

    clientData.map(item => {
    const option = document.createElement('option')
    option.textContent = item.client_name
    option.setAttribute('value', item.id)
    clientSelect.appendChild(option)
    })
    }
})
const stationSelect = document.getElementById('id_station_id')
const  date = new Date()
console.log(date.getFullYear()%1000)
const currentYear = date.getFullYear()%1000
// const stationText = document.getElementsByClassName('station')
clientSelect.addEventListener('change', ev => {
    const selectedClient = ev.target.value
    const textselectedClient = ev.target[selectedClient].outerText

    console.log(ev)
    stationSelect.innerHTML = ""
    
    $.ajax({
        type: 'GET',
        url: `/get-station/${selectedClient}`,
        success: function (response) {
            const stationData = response.data
            stationData.map(item => {
                const option = document.createElement('option')
                option.textContent = item.station_name
                option.setAttribute('value', item.client_id)
                stationSelect.appendChild(option)
                console.log(item.station_name)
            })
        }
    })
        $(document).ready(function () {
            console.log(textselectedClient)
            $("#id_ndi").inputmask(`9999/${textselectedClient}/${currentYear}`, {
                "placeholder": `____/${textselectedClient}/${currentYear}`,
                "onincomplete": function () {
                    return false
                }
            })
        })

})
const ndiBox = document.getElementById('id_ndi')

