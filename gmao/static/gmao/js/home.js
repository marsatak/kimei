$(document).ready(function () {
    let doleanceTable;
    let personnelTable;

    function initDoleanceTable() {
        if ($('#demandeencours').length && !$.fn.DataTable.isDataTable('#demandeencours')) {
            doleanceTable = $('#demandeencours').DataTable({
                ajax: {
                    url: "/home/getDoleanceEncours",
                    dataSrc: ""
                },
                columns: [
                    {data: "id"},
                    {data: "ndi"},
                    {
                        data: 'date_transmission',
                        render: function (data) {
                            return moment(data).format('DD/MM/YYYY HH:mm');
                        }
                    },
                    {data: "statut"},
                    {data: "station.libelle_station"},
                    {data: 'element'},
                    {data: 'panne_declarer'},
                    {
                        data: 'date_deadline',
                        render: function (data) {
                            return data ? moment(data).format('DD/MM/YYYY HH:mm') : '';
                        }
                    },
                    {data: 'commentaire'},
                    {
                        data: null,
                        render: function (data, type, row) {
                            if (row.statut === 'NEW' || row.statut === 'ATD' || row.statut === 'ATP') {
                                return '<button class="btn btn-primary btn-sm declencher-intervention" data-id="' + row.id + '">Déclencher intervention</button>';
                            }
                            return '';
                        }
                    },
                ],
                responsive: true,
                autoWidth: false,
                pageLength: 10,
                language: {
                    url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
                },
                dom: 'Bfrtip',
                buttons: [
                    {
                        extend: 'excel',
                        text: 'Exporter en Excel',
                        exportOptions: {
                            columns: ':visible'
                        }
                    },
                ],
                ordering: false,
                columnDefs: [
                    {
                        targets: [0],
                        visible: false,
                        searchable: false
                    },
                    {responsivePriority: 1, targets: 1},
                    {responsivePriority: 2, targets: 3},
                    {responsivePriority: 3, targets: 6},
                ],
            });
        }
    }

    function initPersonnelTable() {
        if ($('#personnel').length && !$.fn.DataTable.isDataTable('#personnel')) {
            personnelTable = $('#personnel').DataTable({
                ajax: {
                    url: "/home/getPersonnel/",
                    dataSrc: ""
                },
                columns: [
                    {data: "id"},
                    {data: "nom_personnel"},
                    {data: "prenom_personnel"},
                    {
                        data: "statut",
                        render: function (data) {
                            const statuts = {
                                'PRS': '<span class="badge bg-success">Présent</span>',
                                'ABS': '<span class="badge bg-danger">Absent</span>',
                                'ATT': '<span class="badge bg-warning">Tâche attribuée</span>',
                                'INT': '<span class="badge bg-info">En intervention</span>'
                            };
                            return statuts[data] || data;
                        }
                    },
                    {
                        data: null,
                        render: function (data, type, row) {
                            if (row.statut === 'ABS') {
                                return '<button class="btn btn-success btn-sm mark-arrivee" data-id="' + row.id + '">Marquer arrivée</button>';
                            } else if (row.statut === 'PRS') {
                                return '<button class="btn btn-danger btn-sm mark-depart" data-id="' + row.id + '">Marquer départ</button>';
                            }
                            return '';
                        }
                    }
                ],
                responsive: true,
                autoWidth: false,
                pageLength: 10,
                ordering: false,
                language: {
                    url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
                },
                columnDefs: [
                    {
                        targets: [0],
                        visible: false,
                        searchable: false,
                    },
                ],
            });
        }
    }

    if ($('#demandeencours').length && USER_ROLE === 'ADMIN') {
        initDoleanceTable();
        initPersonnelTable();
    }

    $('#demandeencours').on('click', '.declencher-intervention', function () {
        const doleanceId = $(this).data('id');
        declencherIntervention(doleanceId);
    });

    $('#personnel').on('click', '.mark-arrivee, .mark-depart', function () {
        const personnelId = $(this).data('id');
        const isArrivee = $(this).hasClass('mark-arrivee');
        markArriveeOrDepart(personnelId, isArrivee);
    });

    function declencherIntervention(doleanceId) {
        // Implémentez la logique pour déclencher une intervention
    }

    function markArriveeOrDepart(personnelId, isArrivee) {
        // Implémentez la logique pour marquer l'arrivée ou le départ
    }

    function getCookie(name) {
        // Implémentation de getCookie
    }
});