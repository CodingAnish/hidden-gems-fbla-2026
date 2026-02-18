package com.hiddengems.service;

import com.hiddengems.dto.BusinessDto;
import com.hiddengems.entity.Business;
import com.hiddengems.repository.BusinessRepository;
import com.hiddengems.repository.FavoriteRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class BusinessService {

    private final BusinessRepository businessRepository;
    private final FavoriteRepository favoriteRepository;

    public BusinessService(BusinessRepository businessRepository, FavoriteRepository favoriteRepository) {
        this.businessRepository = businessRepository;
        this.favoriteRepository = favoriteRepository;
    }

    public Page<BusinessDto> findAll(Pageable pageable, Long currentUserId) {
        return businessRepository.findAll(pageable)
                .map(b -> toDto(b, currentUserId));
    }

    public Optional<BusinessDto> findById(Long id, Long currentUserId) {
        return businessRepository.findById(id)
                .map(b -> toDto(b, currentUserId));
    }

    public Page<BusinessDto> findByCity(String city, Pageable pageable, Long currentUserId) {
        return businessRepository.findByCity(city, pageable)
                .map(b -> toDto(b, currentUserId));
    }

    public Page<BusinessDto> searchByName(String name, Pageable pageable, Long currentUserId) {
        return businessRepository.findByNameContainingIgnoreCase(name, pageable)
                .map(b -> toDto(b, currentUserId));
    }

    private BusinessDto toDto(Business b, Long userId) {
        BusinessDto dto = new BusinessDto();
        dto.setId(b.getId());
        dto.setName(b.getName());
        dto.setCategory(b.getCategory());
        dto.setAddress(b.getAddress());
        dto.setCity(b.getCity());
        dto.setState(b.getState());
        dto.setZip(b.getZip());
        dto.setPhone(b.getPhone());
        dto.setDescription(b.getDescription());
        dto.setRating(b.getRating());
        dto.setReviewCount(b.getReviewCount());
        dto.setFavorited(userId != null && favoriteRepository.existsByUserIdAndBusinessId(userId, b.getId()));
        return dto;
    }
}
