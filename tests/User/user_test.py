import pytest
class TestUser:
    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data).json()

        assert response.get("id") and response["id"] != "", "ID должен быть не пустым"
        assert response.get("email") == creation_user_data.email
        assert response.get("fullName") == creation_user_data.fullName
        assert response.get("roles", []) == creation_user_data.roles
        assert response.get("verified") is True

    # @pytest.mark.skip(reason="Временно отключен")
    # @pytest.mark.xfail(reason="Функция ещё не реализована")
    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user_response = super_admin.api.user_api.create_user(creation_user_data, expected_status=201).json()
        response_by_id = super_admin.api.user_api.get_user(created_user_response["id"], expected_status=200).json()
        response_by_email = super_admin.api.user_api.get_user(created_user_response["email"], expected_status=200).json()

        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        assert response_by_id.get('id') and response_by_id['id'] != '', "ID должен быть не пустым"
        assert response_by_id.get('email') == creation_user_data.email
        assert response_by_id.get('fullName') == creation_user_data.fullName
        assert response_by_id.get('roles', []) == creation_user_data.roles
        assert response_by_id.get('verified') is True

    @pytest.mark.slow
    def test_get_user_forbidden(self, common_user):
        common_user.api.user_api.get_user(common_user.email, expected_status=403)