/*function initPortfolioTable(data) {
      if ($('#portfolioTable').length) {
          if ($.fn.DataTable.isDataTable('#portfolioTable')) {
              $('#portfolioTable').DataTable().destroy();
          }

          $('#portfolioTable').DataTable({
              data: data,
              columns: [
                  {data: 'ndi'},
                  {data: 'station'},
                  {data: 'element'},
                  {data: 'panne_declarer'},
                  {data: 'statut'},
                  {
                      data: null,
                      render: function (data, type, row) {
                          return getActionButton(row);
                      }
                  }
              ],
              responsive: true,
              autoWidth: false,
              language: {
                  url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
              },
              order: [[0, 'asc']]
          });
      }
  }*/

/*function initPortfolioTable(data) {
    if ($('#portfolioTable').length) {
        if ($.fn.DataTable.isDataTable('#portfolioTable')) {
            $('#portfolioTable').DataTable().destroy();
        }

        $('#portfolioTable').DataTable({
            data: data,
            columns: [
                {data: 'ndi'},
                {data: 'station'},
                {data: 'element'},
                {data: 'panne_declarer'},
                {data: 'statut'},
                {
                    data: null,
                    render: function (data, type, row) {
                        return getActionButton(row);
                    },
                    className: 'action-cell'
                }
            ],
            responsive: {
                details: {
                    display: $.fn.dataTable.Responsive.display.childRowImmediate,
                    type: 'none',
                    target: ''
                }
            },
            autoWidth: false,
            language: {
                url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
            },
            columnDefs: [
                {responsivePriority: 1, targets: 0},
                {responsivePriority: 2, targets: -1},
                {responsivePriority: 3, targets: 4}
            ],
            order: [[0, 'asc']]
        });
    }
}*/
/*function getActionButton(doleance, hasOngoingIntervention) {
      if ((doleance.statut === 'ATT' || doleance.statut === 'INT') && doleance.intervention_id) {
          return `<a href="/home/intervention/${doleance.intervention_id}/" class="btn btn-primary btn-sm w-100">Détails intervention</a>`;
      } else if ((doleance.statut === 'NEW' || doleance.statut === 'ATD' || doleance.statut === 'ATP') && !hasOngoingIntervention) {
          return `<button class="btn btn-success btn-sm w-100 prendre-en-charge" data-id="${doleance.id}">Prendre en charge</button>`;
      } else {
          return '<span class="text-muted">Aucune action disponible</span>';
      }
  }*/
// function getActionButton(doleance) {
//     if ((doleance.statut === 'ATT' || doleance.statut === 'INT') && doleance.intervention_id) {
//         return `<a href="/home/intervention/${doleance.intervention_id}/" class="btn btn-primary btn-sm btn-block">Détails intervention</a>`;
//     } else if (doleance.statut === 'NEW' || doleance.statut === 'ATD' || doleance.statut === 'ATP') {
//         return `<button class="btn btn-success btn-sm btn-block prendre-en-charge" data-id="${doleance.id}">Prendre en charge</button>`;
//     } else {
//         return '<span class="text-muted">Aucune action disponible</span>';
//     }
// }
/*function initPortfolioTable(data, interventionEnCours) {
    if ($('#portfolioContainer').length) {
        if ($.fn.DataTable.isDataTable('#portfolioTable')) {
            $('#portfolioTable').DatterventaTable().destroy();
        }
        let tableHtml = '<table id="portfolioTable" class="table table-striped">';
        tableHtml += '<thead><tr><th>NDIZ</th><th>Station</th><th>Élément</th><th>Panne</th><th>Statut</th><th>Actions</th></tr></thead><tbody>';

        const interventionEnCours = data.some(doleance => doleance.statut === 'ATT' || doleance.statut === 'INT');

        data.forEach(function (doleance) {
            tableHtml += `<tr>
                <td>${doleance.ndi}</td>
                <td>${doleance.station}</td>
                <td>${doleance.element}</td>
                <td>${doleance.panne_declarer}</td>
                <td>${doleance.statut}</td>
                <td>${getActionButton(doleance, interventionEnCours)}</td>
            </tr>`;
        });

        tableHtml += '</tbody></table>';
        $('#portfolioContainer').html(tableHtml);

        $('#portfolioTable').DataTable({
            responsive: true,
            language: {
                url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
            }
        });
    }
}*/

/*function getActionButton(doleance, hasOngoingIntervention) {
    if (doleance.statut === 'ATT' && doleance.intervention_id) {
        return `<a href="/home/intervention/${doleance.intervention_id}/" class="btn btn-primary btn-sm">Détails intervention</a>`;
    } else if ((doleance.statut === 'NEW' || doleance.statut === 'ATD' || doleance.statut === 'ATP') && !hasOngoingIntervention) {
        return `<button class="btn btn-success btn-sm prendre-en-charge" data-id="${doleance.id}">Prendre en charge</button>`;
    } else {
        return '<span class="text-muted">Aucune action disponible</span>';
    }
}*/
function initPortfolioTable(data) {
    if ($('#portfolioTable').length) {
        if ($.fn.DataTable.isDataTable('#portfolioTable')) {
            $('#portfolioTable').DataTable().destroy();
        }

        $('#portfolioTable').DataTable({
            data: data,
            columns: [
                {data: 'ndi', width: "10%"},
                {data: 'station', width: "15%"},
                {data: 'element', width: "15%"},
                {data: 'panne_declarer', width: "30%", className: 'panne-cell'},
                {data: 'statut', width: "10%"},
                {
                    data: null,
                    render: function (data, type, row) {
                        return getActionButton(row, interventionEnCours);
                    },
                    width: "20%",
                    className: 'action-cell'
                }
            ],
            responsive: true,
            autoWidth: false,
            language: {
                url: '//cdn.datatables.net/plug-ins/1.10.24/i18n/French.json'
            },
            columnDefs: [
                {responsivePriority: 1, targets: 0}, // NDI
                {responsivePriority: 2, targets: -1}, // Actions
                {responsivePriority: 3, targets: 4}, // Statut
                {
                    targets: '_all',
                    render: function (data, type, row) {
                        if (type === 'display') {
                            return '<div class="text-wrap width-100">' + data + '</div>';
                        }
                        return data;
                    }
                }
            ],
            order: [[0, 'asc']],
            drawCallback: function (settings) {
                // Ajuster la hauteur des lignes après le rendu
                $('#portfolioTable tbody tr').each(function () {
                    var highestBox = 0;
                    $(this).find('td').each(function () {
                        if ($(this).height() > highestBox) {
                            highestBox = $(this).height();
                        }
                    });
                    $(this).find('td').height(highestBox);
                });
            }
        });
    }
}

function getActionButton(doleance, interventionEnCours) {
    if ((doleance.statut === 'ATT' || doleance.statut === 'INT') && doleance.intervention_id) {
        return `<a href="/home/intervention/${doleance.intervention_id}/" class="btn btn-primary btn-sm btn-block">Détails intervention</a>`;
    } else if ((doleance.statut === 'NEW' || doleance.statut === 'ATD' || doleance.statut === 'ATP') && !interventionEnCours) {
        return `<button class="btn btn-success btn-sm btn-block prendre-en-charge" data-id="${doleance.id}">Prendre en charge</button>`;
    } else {
        return '<span class="text-muted">Aucune action disponible</span>';
    }
}
