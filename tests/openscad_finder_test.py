import unittest
from unittest.mock import patch, MagicMock
import datetime
import os
from anchorscad_lib.utils.openscad_finder import (
    OpenscadExeSignature,
    OpenscadProperties,
    CachedData,
    get_features_from_exe,
    openscad_exe_properties
)

class TestOpenscadFinder(unittest.TestCase):
    
    def test_openscad_exe_signature(self):
        # Test signature creation and comparison
        test_exe = "/usr/bin/openscad"
        test_date = datetime.datetime(2024, 1, 1)
        test_size = 1000
        
        sig = OpenscadExeSignature(test_exe, test_date, test_size)
        
        self.assertEqual(sig.exe, test_exe)
        self.assertEqual(sig.modified, test_date)
        self.assertEqual(sig.size, test_size)
        self.assertEqual(sig.version, OpenscadExeSignature.THIS_VERSION)
        
    def test_openscad_properties_dev_options(self):
        # Test dev options with manifold backend
        sig = OpenscadExeSignature.make_default()
        props = OpenscadProperties(sig, {'lazy-union'}, True)
        
        self.assertEqual(
            props.dev_options(), 
            ('--backend', 'Manifold', '--enable', 'lazy-union'))
        
        # Test dev options with manifold feature
        props = OpenscadProperties(sig, {'manifold', 'lazy-union'}, False)
        self.assertEqual(
            props.dev_options(), 
            ('--enable', 'manifold', '--enable', 'lazy-union'))
        
        # Test dev options with no manifold
        props = OpenscadProperties(sig, {'lazy-union'}, False)
        self.assertEqual(props.dev_options(), ('--enable', 'lazy-union'))
        
    @patch('anchorscad_lib.utils.openscad_finder.Popen')
    def test_get_features_from_exe(self, mock_popen):
        # Mock the openscad --help output
        mock_process = MagicMock()
        mock_process.communicate.return_value = (None, b'''
        --enable experimental features:
            lazy-union | fast-csg | fast-csg-trust-corefinement
            | fast-csg-exact | fast-csg-exact-callbacks
        
        --backend arg                     3D rendering backend to use: 'CGAL'
                                         (old/slow) [default] or 'Manifold'
                                         (new/fast)
        ''')
        mock_process.wait.return_value = 0
        mock_popen.return_value = mock_process
        
        # Mock the Popen constructor to avoid file system checks
        mock_popen.side_effect = lambda args, executable, stdout, stderr: mock_process
        
        features, has_manifold = get_features_from_exe('/usr/bin/openscad')
        
        self.assertTrue('lazy-union' in features)
        self.assertFalse('manifold' in features)
        self.assertTrue(has_manifold)
        
        # Verify Popen was called correctly
        mock_popen.assert_called_once_with(
            args=['openscad', '--help'],
            executable='/usr/bin/openscad',
            stdout=-1,
            stderr=-1)

    @patch('shutil.which')
    @patch('anchorscad_lib.utils.openscad_finder.get_features_from_exe')
    @patch('anchorscad_lib.utils.openscad_finder.store_cache')
    @patch('anchorscad_lib.utils.openscad_finder.load_cache')
    def test_openscad_exe_properties_from_path(
            self, mock_load_cache, mock_store_cache, 
            mock_get_features, mock_which):
        # Mock finding openscad in PATH
        mock_which.return_value = '/usr/bin/openscad'
        mock_get_features.return_value = ({'lazy-union', 'manifold'}, True)
        
        # Mock cache operations
        mock_load_cache.return_value = CachedData()
        
        # Mock os.stat for the exe signature
        stat_result = os.stat(__file__)  # Use this file's stats as a mock
        with patch('os.stat') as mock_stat:
            mock_stat.return_value = stat_result
            
            # Get properties
            props = openscad_exe_properties()
            
            self.assertEqual(props.exe, '/usr/bin/openscad')
            self.assertEqual(props.features, {'lazy-union', 'manifold'})
            self.assertTrue(props.backend_has_manifold)
            
            # Verify the mocks were called
            mock_which.assert_called_once_with('openscad')
            mock_get_features.assert_called_once_with('/usr/bin/openscad')
            mock_load_cache.assert_called_once()
            mock_store_cache.assert_called_once()

if __name__ == '__main__':
    unittest.main()
