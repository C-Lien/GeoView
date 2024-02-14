# pyqtgraph libraries
import pyqtgraph.opengl as gl


class CreateGrid():
    ''' Class in orphon state.
        Awating refactor and reintegration.
    '''

    def set_grid_coord(self, pos_data, euc_center, grid_dims):
        """
            NOT IN USE----------------------------------------------------------
            Add a Grid- This is laggy. Consider adding as a boolean button.
        """
        grid = self.create_grid(pos_data, euc_center, *grid_dims)
        self.view3d.addItem(grid)

    def create_grid(self, pos_data, euc_center, grid_dims):
        """
            NOT IN USE----------------------------------------------------------
            Add a Grid at the centre of the selected data and set the size to
            encompass all loaded boreholes.
        """
        grid = gl.GLGridItem()
        grid.setParentItem(pos_data)
        grid.translate(euc_center[0], euc_center[1], 0.0)
        grid.setSize(x=grid_dims[0], y=grid_dims[1], z=0.0)

        return grid