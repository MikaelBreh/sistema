    document.addEventListener('DOMContentLoaded', function() {
        document.getElementById('cliente_input').addEventListener('input', function() {
            var selectedOption = document.querySelector('option[value="' + this.value + '"]');
            if (selectedOption) {
                var id = selectedOption.getAttribute('data-id');
                var cnpj = selectedOption.getAttribute('data-cnpj');
                var endereco = selectedOption.getAttribute('data-endereco');
                var inscricao_estadual = selectedOption.getAttribute('data-ie');
                document.getElementById('info_cliente').innerHTML = "<p>CNPJ: " + cnpj + " - Inscrição Estadual: " + inscricao_estadual + "</p><p>Endereço: " + endereco + "</p>";
                document.getElementById('cliente_id').value = id;
            } else {
                document.getElementById('info_cliente').innerHTML = "";
                document.getElementById('cliente_id').value = "";
            }
        });
    });