async function loadTickets() {

    const response = await fetch(
        "http://127.0.0.1:8000/tickets"
    );

    const tickets = await response.json();

    const table = document.getElementById(
        "ticketTable"
    );

    table.innerHTML = "";

    tickets.forEach(ticket => {

        const row = `
            <tr>
                <td>${ticket.ticket_id}</td>
                <td>${ticket.customer_name}</td>
                <td>${ticket.category}</td>
                <td>${ticket.priority_raw}</td>
                <td>${ticket.status}</td>
                <td>${ticket.sla_breached}</td>
            </tr>
        `;

        table.innerHTML += row;
    });
}