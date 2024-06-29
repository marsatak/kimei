/*
const idclientBox = document.getElementById('id_client_id')
const idstationBox = document.getElementById('id_station_id')
const idcontracttypeBox = document.getElementById('id_contract_type')
const idndiBox = document.getElementById('id_ndi')
// console.log(idclientBox)

idclientBox.addEventListener('input', (ev) => {
    const selectedClient = ev.target.value
    const textselectedClient = ev.target[selectedClient].innerText
    // const contractType = idcontracttypeBox.option.selected
    const date = new Date()
    const currentYear = date.getFullYear() % 1000
    console.log('test', idndiBox.textContent)
    // id_contract_type
    $.ajax({
        type: 'GET',
        url: `/get-station/${selectedClient}`,
        success: function (response) {
            // console.log(response.data)
            const stationData = response.data
            
            idstationBox.innerHTML = ""
            const option = document.createElement('option')
            option.textContent = "-------"
            stationData.map(item => {
                // option.textContent="---------"
                // option.setAttribute('selected', 'true')
                // option.setAttribute('value', item.client_id)
                const option = document.createElement('option')
                option.textContent = item.station_name
                idstationBox.appendChild(option)
            })
        }
    })
    idcontracttypeBox.addEventListener('input', (ctype) => {
        console.log(ctype.target.value)
        console.log('test', idndiBox.textContent)
        
        const typecontrat = ctype.target.value
        $(document).ready(function () {
            console.log(textselectedClient)
            $("#id_ndi").inputmask(`9999/${textselectedClient}/${currentYear}${typecontrat}`, {
                "placeholder": `____/${textselectedClient}/${currentYear}${typecontrat}`,
                "onincomplete": function () {
                    return false
                }
            })
        })
    })
})*/
