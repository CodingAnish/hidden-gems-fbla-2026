package com.hiddengems.repository;

import com.hiddengems.entity.Business;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface BusinessRepository extends JpaRepository<Business, Long> {

    Page<Business> findByCategoryIgnoreCase(String category, Pageable pageable);
    Page<Business> findByNameContainingIgnoreCase(String name, Pageable pageable);
    List<Business> findByCityIgnoreCaseOrderByName(String city);

    @Query("SELECT b FROM Business b WHERE LOWER(b.city) = LOWER(:city)")
    Page<Business> findByCity(@Param("city") String city, Pageable pageable);
}
