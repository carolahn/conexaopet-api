import os

def change_image_permissions(image_path, permissions):
    """
    Altera as permissões de um arquivo de imagem.

    Args:
        image_path (str): O caminho do arquivo de imagem.
        permissions (int): As permissões desejadas.

    Returns:
        bool: True se as permissões foram alteradas com sucesso, False caso contrário.
    """
    try:
        # Obtém as permissões atuais do arquivo
        current_permissions = os.stat(image_path).st_mode

        # Altera as permissões do arquivo
        os.chmod(image_path, permissions)

        # Verifica se as permissões foram alteradas corretamente
        if os.stat(image_path).st_mode == permissions:
            return True
        else:
            return False
    except Exception as e:
        print(f"Erro ao alterar permissões do arquivo: {e}")
        return False