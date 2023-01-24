import unittest
from unittest.mock import MagicMock, patch
import argparse
import atmos

class DetermineActionsTests(unittest.TestCase):

    def setUp(self):
        self.input_args = argparse.Namespace(command="mytestcommand", e=False, m=False, n=False, project="", verbose=False)
        atmos.is_git_directory = MagicMock(return_value=False)
        atmos.run_cmd = MagicMock()

    def test_whenCalledWithNoAdditionalArgs_shouldRunTheTerraformCommand(self):
        """Simplest case where atmos is only called with a command and no further arguments"""
        atmos.determine_actions(self.input_args, [])
        atmos.run_cmd.assert_called_with("terraform mytestcommand")

    def test_whenCalledWithParams_theyAreAppended(self):
        """Should append all params after the command"""
        atmos.determine_actions(self.input_args, ["--myparam", "myvalue"])
        atmos.run_cmd.assert_called_with("terraform mytestcommand --myparam myvalue")

    @patch("workspaces.get_env")
    def test_whenCalledWithInitCommand_shouldAppendVarsAndCreds(self, mocked_get_env):
        """Case where var-file, -var workpace=xyz is appended"""
        self.input_args.command = "init"
        mocked_get_env.return_value = "mytestenv"
        atmos.determine_actions(self.input_args, [])
        atmos.run_cmd.assert_called_with('terraform init -var-file=vars/mytestenv.tfvars -var "workspace=mytestenv"')

    @patch("workspaces.get_env")
    def test_whenCalledWithPlanCommand_shouldAppendVarsAndCreds(self, mocked_get_env):
        """Case where var-file, -var workpace=xyz is appended"""
        self.input_args.command = "plan"
        mocked_get_env.return_value = "mytestenv"
        atmos.determine_actions(self.input_args, [])
        atmos.run_cmd.assert_called_with('terraform plan -var-file=vars/mytestenv.tfvars -var "workspace=mytestenv"')

    @patch("workspaces.get_env")
    def test_whenCalledWithApplyCommand_shouldAppendVarsAndCreds(self, mocked_get_env):
        """Case where var-file, -var workpace=xyz is appended"""
        self.input_args.command = "apply"
        mocked_get_env.return_value = "mytestenv"
        atmos.determine_actions(self.input_args, [])
        atmos.run_cmd.assert_called_with('terraform apply -var-file=vars/mytestenv.tfvars -var "workspace=mytestenv"')

    @patch("workspaces.get_env")
    def test_whenCalledWithDestroyCommand_shouldAppendVarsAndCreds(self, mocked_get_env):
        """Case where var-file, -var workpace=xyz is appended"""
        self.input_args.command = "destroy"
        mocked_get_env.return_value = "mytestenv"
        atmos.determine_actions(self.input_args, [])
        atmos.run_cmd.assert_called_with('terraform destroy -var-file=vars/mytestenv.tfvars -var "workspace=mytestenv"')

    @patch("workspaces.workspace_manager")
    def test_whenInAGitRepo_andManualArgIsNotGiven_andEnvironmentArgIsNotGiven_shouldCallTheWorkspaceManager(self, mocked_workspace_manager):
        atmos.is_git_directory.return_value = True
        atmos.determine_actions(self.input_args, [])
        mocked_workspace_manager.assert_called_once()

    @patch("credentials.generate")
    def test_whenEnvironmentArgIsGiven_shouldGenerateCredentials(self, mocked_generate):
        self.input_args.e = True
        atmos.determine_actions(self.input_args, [])
        mocked_generate.assert_called_once()


if __name__ == '__main__':
    unittest.main()
