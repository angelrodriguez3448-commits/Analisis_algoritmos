#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>

namespace py = pybind11;

std::vector<int> buscar_patron_binario(const std::vector<int>& texto, const std::vector<int>& patron) {
    std::vector<int> posiciones;
    int n = texto.size(), m = patron.size();
    if (n < m) return posiciones;

    for (int i = 0; i <= n - m; ++i) {
        bool coincide = true;
        for (int j = 0; j < m; ++j) {
            if (texto[i + j] != patron[j]) {
                coincide = false;
                break;
            }
        }
        if (coincide) posiciones.push_back(i);
    }
    return posiciones;
}
#include <vector>

std::vector<int> divide_and_conquer_search(const std::vector<int>& texto, const std::vector<int>& patron, int start = 0) {
    int n = texto.size(), m = patron.size();
    std::vector<int> posiciones;

    if (n < m) {
        return posiciones;
    } else if (n <= 2 * m) {
        for (int i = 0; i <= n - m; ++i) {
            bool coincide = true;
            for (int j = 0; j < m; ++j) {
                if (texto[i + j] != patron[j]) {
                    coincide = false;
                    break;
                }
            }
            if (coincide) posiciones.push_back(start + i);
        }
        return posiciones;
    } else {
        int mid = n / 2;
        std::vector<int> left = divide_and_conquer_search(
            std::vector<int>(texto.begin(), texto.begin() + mid + m - 1),
            patron,
            start
        );
        std::vector<int> right = divide_and_conquer_search(
            std::vector<int>(texto.begin() + mid, texto.end()),
            patron,
            start + mid
        );
        posiciones.insert(posiciones.end(), left.begin(), left.end());
        posiciones.insert(posiciones.end(), right.begin(), right.end());
        return posiciones;
    }
}


PYBIND11_MODULE(busqueda, m) {
    m.def("buscar_patron_binario", &buscar_patron_binario, "Buscar patrón binario en texto comprimido");
    m.def("divide_and_conquer_search", &divide_and_conquer_search, "Búsqueda binaria por divide y vencerás");
}

