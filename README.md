# Lake Graphics Framework

**Python 3D Library.**

A generic and simple 3D library based on OpenGL and glfw, allowing easy development of graphical software.

### Dependencies

Linux and Windows 10+ support.

### Usage

I'll add a discription later!   ;3

```
import graphics, physics

fov, aspect, near, far = 90, 16/9, 0.1, 200

create scene # TODO
create window # TODO

create camera.perspective(fov, aspect, near, far)
create shader
camera.apply_shader(shader)

geometry = BoxGeometry((1, 1, 1))
material = MeshBasicMaterial({"color": (200, 150, 150)})
cube = Mesh(geometry, material)
cube.move_to((1, 0, 0))
scene.add(cube)
cube.move((2, 0, 0))

object = EmptyObject()
scene.add(object)

geometry = SphereGeometry( some settings ) # TODO
sphere = Mesh(geometry, material)
cube.add(sphere)
sphere.move((1, 0, 0))

material.set_color((100, 100, 100))

sphere.get_parent().move((1, 0, 0))

camera.look_at(object)

window.set_viewport(0, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT)
window.clear()
window.render(scene, camera)
window.update()
```

## Authors

Tequin Lake
[@Laketequin1](https://awsnap.dev/)

## License

TODO :)

## Acknowledgments

Inspiration from [three.js](https://github.com/mrdoob/three.js)