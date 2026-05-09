document.addEventListener('DOMContentLoaded', function() {
    console.log("JS загружен, начинаем сбор данных...");
    loadDriverStandings();
    loadWCC();
});

async function loadDriverStandings() {
    try {
        const response = await fetch('/standings/drivers');
        const data = await response.json();
        const tableBody = document.querySelector('#drivers-standings tbody');

        tableBody.innerHTML = '';

        data.forEach(item => {
            const row = `
                <tr>
                    <td><span class="badge ${item.rank <= 3 ? 'bg-danger' : 'bg-secondary'}">${item.rank}</span></td>
                    <td class="fw-bold">${item.full_name}</td>
                    <td>${item.team_name}</td>
                    <td class="text-danger fw-bold">${item.total_points}</td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    } catch (error) {
        console.error('Ошибка при получении зачета пилотов:', error);
    }
}

async function loadWCC() {
    try {
        const response = await fetch('/standings/wcc/2024');
        const data = await response.json();
        const tableBody = document.querySelector('#wcc-standings tbody');

        tableBody.innerHTML = '';

        if (data.message) {
             tableBody.innerHTML = `<tr><td colspan="2" class="text-center">${data.message}</td></tr>`;
             return;
        }

        data.forEach(item => {
            const row = `
                <tr>
                    <td class="text-uppercase">${item.team}</td>
                    <td class="text-danger fw-bold">${item.points}</td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    } catch (error) {
        console.error('Ошибка при получении WCC:', error);
    }
}