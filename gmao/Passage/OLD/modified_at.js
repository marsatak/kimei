let lastUpdateTimestamp = localStorage.getItem('lastUpdateTimestamp') || null;

function loadData() {
    $.ajax({
        url: '/api/data',
        method: 'GET',
        data: {last_update: lastUpdateTimestamp},
        success: function (response) {
            if (response.hasNewData) {
                updateTables(response.data);
                localStorage.setItem('lastUpdateTimestamp', response.timestamp);
            }
        }
    });
}

function updateTables(data) {
    if (data.doleances) {
        $('#demandeencours').DataTable().clear().rows.add(data.doleances).draw();
    }
    if (data.interventions) {
        $('#interventions').DataTable().clear().rows.add(data.interventions).draw();
    }
    if (data.personnel) {
        $('#personnel').DataTable().clear().rows.add(data.personnel).draw();
    }
}

$(document).ready(function () {
    loadData();

    // Rafraîchir les données toutes les 5 minutes
    setInterval(loadData, 300000);
});