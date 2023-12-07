
mock_user = {
    'discord_id': '112233'
}

mock_register = {
    'discord_id': '334455',
    'matricula': '112233'
}

mock_turma = {
    "denominacao": "LOP_Orivaldo",
    "ano": 2023,
    "periodo": 2,
    "data_inicio": "2023-10-02",
    "data_fim": "2023-12-01",
    "alunos": [
        {
            "nome": "Joao",
            "matricula": "112233",
            "turma": "2A"
        },
        {
            "nome": "Maria",
            "matricula": "112234",
            "turma": "1B"
        }
    ]
}

mock_alunos = [
    {
        "nome": "Pedro",
        "matricula": "112235",
        "turma": "1C"
    },
    {
        "nome": "Joana",
        "matricula": "112236",
        "turma": "2B"
    }
]

mock_testes = [
    {
        'teste_id': 'T01',
        'pergunta': 'Quanto e 2+2?',
        'resposta': 'B',
        'alternativas': {
            'A': '2',
            'B': '4',
            'C': '5',
            'D': '0'
        }
    },
    {
        'teste_id': 'T02',
        'pergunta': 'Em que ano o Brasil foi descoberto?',
        'resposta': 'D',
        'alternativas': {
            'A': '1400',
            'B': '1300',
            'C': '2023',
            'D': '1500'
        }
    }
]

mock_teste_resposta_correta = {
    'teste_id': 'T01',
    'opcao': 'B'
}

mock_teste_resposta_errada = {
    'teste_id': 'T01',
    'opcao': 'C'
}