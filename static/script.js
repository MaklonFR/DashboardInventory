function setStatus(status) {
    document.getElementById('status').textContent = status;
    if (status == 'ON') {
        document.getElementById('onButton').style.backgroundColor = 'green';
        document.getElementById('offButton').style.backgroundColor = '';
        document.getElementById('status').style.color = 'green';
    } else {
        document.getElementById('onButton').style.backgroundColor = '';
        document.getElementById('offButton').style.backgroundColor ='red';
        document.getElementById('status').style.color ='red';
    }
}

setInterval(updateAll, 1000);
