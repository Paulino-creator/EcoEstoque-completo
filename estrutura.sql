
-- Criar o banco EcoEstoque
CREATE DATABASE IF NOT EXISTS ecoestoque
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE ecoestoque;


-- TABELA 1: USUÁRIOS
CREATE TABLE IF NOT EXISTS USUARIO (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome_usuario VARCHAR(150) NOT NULL,
    cpf VARCHAR(14),
    email VARCHAR(150) UNIQUE,
    matricula VARCHAR(50) UNIQUE,
    tipo_usuario ENUM('aluno', 'professor', 'admin') NOT NULL
) ENGINE=InnoDB;


-- TABELA 2: CATEGORIAS
CREATE TABLE IF NOT EXISTS CATEGORIA (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nome_categoria VARCHAR(100) NOT NULL UNIQUE,
    descricao_categoria VARCHAR(255)
) ENGINE=InnoDB;


-- TABELA 3: LOCALIZAÇÕES
CREATE TABLE IF NOT EXISTS LOCALIZACAO (
    id_localizacao INT AUTO_INCREMENT PRIMARY KEY,
    bloco VARCHAR(50) NOT NULL,
    armario VARCHAR(50)
) ENGINE=InnoDB;


-- TABELA 4: MATERIAIS
CREATE TABLE IF NOT EXISTS MATERIAL (
    id_material INT AUTO_INCREMENT PRIMARY KEY,
    codigo_barras VARCHAR(100) UNIQUE,
    nome_material VARCHAR(150) NOT NULL,
    descricao_material VARCHAR(255),
    qtd_total INT NOT NULL DEFAULT 0,
    qtd_disponivel INT NOT NULL DEFAULT 0,
    id_categoria INT NOT NULL,
    id_localizacao INT NOT NULL,

    CONSTRAINT fk_material_categoria
        FOREIGN KEY (id_categoria)
        REFERENCES CATEGORIA(id_categoria),

    CONSTRAINT fk_material_localizacao
        FOREIGN KEY (id_localizacao)
        REFERENCES LOCALIZACAO(id_localizacao),

    CONSTRAINT chk_quantidades
        CHECK (
            qtd_total >= 0
            AND qtd_disponivel >= 0
            AND qtd_disponivel <= qtd_total
        )
) ENGINE=InnoDB;


-- TABELA 5: RESERVAS
CREATE TABLE IF NOT EXISTS RESERVA (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    data_solicitacao DATE NOT NULL,
    data_previsao_retirada DATE NOT NULL,
    status_reserva VARCHAR(50) NOT NULL DEFAULT 'pendente',

    FOREIGN KEY (id_usuario)
        REFERENCES USUARIO(id_usuario)
) ENGINE=InnoDB;


-- TABELA 6: MATERIAIS DE CADA RESERVA
CREATE TABLE IF NOT EXISTS ITEM_RESERVA (
    id_item_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_reserva INT NOT NULL,
    id_material INT NOT NULL,
    qtd_reserva INT NOT NULL CHECK (qtd_reserva > 0),

    FOREIGN KEY (id_reserva)
        REFERENCES RESERVA(id_reserva),

    FOREIGN KEY (id_material)
        REFERENCES MATERIAL(id_material)
) ENGINE=InnoDB;


-- TABELA 7: EMPRÉSTIMOS
CREATE TABLE IF NOT EXISTS EMPRESTIMO (
    id_emprestimo INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario_solicitante INT NOT NULL,
    id_reserva INT,
    data_retirada DATE NOT NULL,
    data_previsao_devolucao DATE NOT NULL,
    data_devolucao DATE,

    FOREIGN KEY (id_usuario_solicitante)
        REFERENCES USUARIO(id_usuario),

    FOREIGN KEY (id_reserva)
        REFERENCES RESERVA(id_reserva)
) ENGINE=InnoDB;


-- TABELA 8: MATERIAIS EMPRESTADOS
CREATE TABLE IF NOT EXISTS ITEM_EMPRESTIMO (
    id_item_emprestimo INT AUTO_INCREMENT PRIMARY KEY,
    id_emprestimo INT NOT NULL,
    id_material INT NOT NULL,
    quantidade_emprestada INT NOT NULL
        CHECK (quantidade_emprestada > 0),
    estado_devolucao VARCHAR(100),
    status_emprestimo VARCHAR(50) NOT NULL DEFAULT 'emprestado',

    FOREIGN KEY (id_emprestimo)
        REFERENCES EMPRESTIMO(id_emprestimo),

    FOREIGN KEY (id_material)
        REFERENCES MATERIAL(id_material)
) ENGINE=InnoDB;



-- TABELA 9: KITS DE MATERIAIS
CREATE TABLE IF NOT EXISTS KIT_MATERIAL (
    id_kit INT AUTO_INCREMENT PRIMARY KEY,
    nome_kit VARCHAR(100) NOT NULL,
    descricao_kit VARCHAR(255)
) ENGINE=InnoDB;


-- TABELA 10: ITENS QUE FORMAM OS KITS
CREATE TABLE IF NOT EXISTS ITEM_KIT (
    id_item_kit INT AUTO_INCREMENT PRIMARY KEY,
    id_kit INT NOT NULL,
    id_material INT NOT NULL,
    quantidade_no_kit INT NOT NULL
        CHECK (quantidade_no_kit > 0),

    FOREIGN KEY (id_kit)
        REFERENCES KIT_MATERIAL(id_kit),

    FOREIGN KEY (id_material)
        REFERENCES MATERIAL(id_material),

    UNIQUE (id_kit, id_material)
) ENGINE=InnoDB;


-- TABELA 11: OCORRÊNCIAS DE AVARIAS
CREATE TABLE IF NOT EXISTS OCORRENCIA_AVARIA (
    id_ocorrencia INT AUTO_INCREMENT PRIMARY KEY,
    id_item_emprestimo INT NOT NULL,
    data_ocorrencia DATE NOT NULL,
    descricao_dano VARCHAR(255) NOT NULL,
    valor_prejuizo DECIMAL(10,2) DEFAULT 0.00,

    FOREIGN KEY (id_item_emprestimo)
        REFERENCES ITEM_EMPRESTIMO(id_item_emprestimo)
) ENGINE=InnoDB;
