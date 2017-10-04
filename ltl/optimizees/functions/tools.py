def plot(fn, random_state):
    """
    Implements plotting of 2D functions generated by FunctionGenerator
    :param fn: Instance of FunctionGenerator
    """
    import numpy as np
    from ltl.matplotlib_ import plt
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator, FormatStrFormatter

    fig = plt.figure()
    ax = fig.gca(projection=Axes3D.name)

    # Make data.
    X = np.arange(fn.bound[0], fn.bound[1], 0.05)
    Y = np.arange(fn.bound[0], fn.bound[1], 0.05)
    XX, YY = np.meshgrid(X, Y)
    Z = [fn.cost_function([x, y], random_state=random_state) for x, y in zip(XX.ravel(), YY.ravel())]
    Z = np.array(Z).reshape(XX.shape)

    # Plot the surface.
    surf = ax.plot_surface(XX, YY, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)

    # Customize the z axis.
    # ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    W = np.where(Z == np.min(Z))
    ax.set(title='Min value is %.2f at (%.2f, %.2f)' % (np.min(Z), X[W[0]], Y[W[1]]))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.savefig('function.png')
    plt.show()
